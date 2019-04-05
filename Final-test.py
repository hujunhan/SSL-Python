import socket
import threading
from SSL_Lib.Robot import Robot
from SSL_Lib.Camera import Camera
from SSL_Lib.DStar import DStar
from SSL_Lib.utils import *
from SSL_Lib.DBG import DBG
from SSL_Lib.DWA1 import *
import serial
import sys
import time

serialPort = "COM4"  # 串口
# 初始化控制和读取的IP地址、端口号
localhost = '127.0.0.1'
control_addr = (localhost, 20011)
read_addr = (localhost, 23333)
camera = Camera(read_addr)
debug = DBG()
# ser=None
# ser = serial.Serial(serialPort, 115200, timeout=0.5)
# ser=config_serial(serialPort)
# 主逻辑


# 1.初始化要控制的机器人
ro_b_0 = Robot('blue', 0, 0.15, control_addr=control_addr)
blue, yellow = camera.getRobotDict()  # 读取初始信息(已换算)
start_point = [blue[0].x, blue[0].y]  # 设置机器人开始的位置(已换算，单位是m)
end_point = [-start_point[0], -start_point[1]]  # 设置机器人终点为对称点(已换算，单位是m)
print('start at: ', start_point)
print('goal at: ', end_point)

# 2.目前只测试静态避障，所以只生成一次路径规划
ob_temp = []
for ro in blue.values():
	if ro.robot_id is not 0:
		ob_temp.append([ro.x, ro.y])
		print(ro.x)
		debug.addCircle(ro.x, ro.y,0.2)
for ro in yellow.values():
	ob_temp.append(([ro.x, ro.y ]))
	debug.addCircle(ro.x, ro.y, 0.2)
ob = np.array(ob_temp)
print('ob = ', ob)
u = np.array([0.0, 0.0])
config = Config()
debug.sendDebugMessage()  # debug信息发送

# 2.1 新建地图
radius = 0.2
path = statics_map(start_point, end_point, blue, yellow, radius)  # 从Dstar获取路径信息
x = np.array([blue[0].x , blue[0].y , blue[0].orientation, 0.0, 0.0])
traj = np.array(x)
while path is None:  # 如果障碍物膨胀太多，就逐渐减小
	radius = radius - 0.01
	if radius < 0.05:
		print('No way out!')
		break
	print('Now trying radius = ', radius)
	path = statics_map(start_point, end_point, blue, yellow, radius)

goal = np.array([path[0].x , path[0].y ])
#print(goal)
#path=path[::10] #精简一下路径


print('get path!')
print('path start at: ', path[0])
print('path end at: ', path[-1])
print('length of path: ', len(path))
print('length of path(reduced): ', len(path))
debug.addPath(path)  # 将路径画出来
debug.sendDebugMessage()  # debug信息发送
#print(path)

i = 0
speed = 1

# 3. 新建一个进程
# 用来另开一个线程的函数
def getblue0():
	global blue
	while True:
		x, y = camera.getRobotDict()
		blue[0] = x[0]


thread1 = threading.Thread(target=getblue0)
thread1.start()

# 4. 主循环
while True:
	# 4.1 根据DWA计算所应该施加的控制指令
	# u[0]是机器人x轴速度，u[1]是机器人y轴速度
	u, ltraj = dwa_control(x, u, config, goal, ob, ro_b_0, camera)
	ro_b_0.setSpeed(u[1], u[0], 0)
	x = np.array([blue[0].x , blue[0].y , blue[0].orientation, blue[0].vel_x , blue[0].vel_y ])
	if math.sqrt((x[0] - goal[0]) ** 2 + (x[1] - goal[1]) ** 2) <= config.robot_radius:
		print("Goal!!")
		i = i + 1
		goal = np.array([path[i].x , path[i].y ])
	#time.sleep(0.015)
# chase2(blue[0],[path_x,path_y],ro_b_0,1,1)
