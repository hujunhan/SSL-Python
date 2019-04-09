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
from SSL_Lib.RRT import *

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

blue, yellow = camera.getRobotDict()  # 读取初始信息
start_point = [blue[0].x, blue[0].y]  # 设置机器人开始的位置
end_point = [-start_point[0], -start_point[1]]  # 设置机器人终点为对称点
print('start at: ', start_point)
print('goal at: ', end_point)

# 2.目前只测试静态避障，所以只生成一次路径规划
ob_temp = []
for ro in blue.values():
	if ro.robot_id is not 0:
		ob_temp.append((ro.x, ro.y, 0.3))
# debug.addCircle(ro.x/10,ro.y/10,20)
for ro in yellow.values():
	ob_temp.append((ro.x, ro.y, 0.3))
# debug.addCircle(ro.x/10,ro.y/10,20)
ob = np.array(ob_temp)
print('ob = ', ob_temp)
u = np.array([0.0, 0.0])
config = Config()
# 2.1 新建地图
starttime = time.time()
rrt = RRT(start=[blue[0].x, blue[0].y], goal=end_point,
		  randArea=[6, 4], obstacleList=ob)
path = rrt.Planning(animation=False)
maxIter = 1000
path = PathSmoothing(path, maxIter, ob_temp)
print('Using ', time.time() - starttime, ' to calculate rrt!')
x = np.array([blue[0].x, blue[0].y, blue[0].orientation, 0.0, 0.0])
traj = np.array(x)
# while path is None:  # 如果障碍物膨胀太多，就逐渐减小
# 	radius = radius - 0.01
# 	if radius < 0.05:
# 		print('No way out!')
# 		break
# 	print('Now trying radius = ', radius)
# 	pf = statics_map(start_point, end_point, blue, yellow, radius)
# 	path=pf.get_path()
print(path)
goal = np.array([path[0][0], path[0][1]])

# path=path[::10] #精简一下路径


print('get path!')
print('path start at: ', path[0])
print('path end at: ', path[-1])
print('length of path: ', len(path))
print('length of path(reduced): ', len(path))
# debug.addPath_rrt(path, 4)  # 将路径画出来
# debug.sendDebugMessage()  # debug信息发送

i = 0
speed = 1


# 3. 新建一个进程
# 用来另开一个线程的函数
def getblue0():
	global blue, yellow, ob
	while True:
		# print('update robot info!')
		# thread2.join()
		blue, yellow = camera.getRobotDict()
		ob_temp1 = []
		for ro in blue.values():
			ob_temp1.append([ro.x, ro.y, 0.3])
		# debug.addCircle(ro.x/10,ro.y/10,20)
		for ro in yellow.values():
			if ro.robot_id is not 0:
				ob_temp1.append(([ro.x, ro.y, 0.3]))
		# debug.addCircle(ro.x/10,ro.y/10,20)
		ob = np.array(ob_temp1)


def checkDanger():
	sx = blue[0].x
	sy = blue[0].y
	gx = goal[0]
	gy = goal[1]
	for ro in ob:
		if ((ro[0] - sx) * (ro[0] - gx)) < 0:
			if ((ro[1] - sy) * (ro[1] - gy)) < 0:
				if checkInLine([sx, sy], [gx, gy], [ro[0], ro[1]], 0.3):
					return True


def checkInLine(a, b, c, r):
	aa = np.hypot(b[0] - c[0], b[1] - c[1])
	bb = np.hypot(a[0] - c[0], a[1] - c[1])
	cc = np.hypot(a[0] - b[0], a[1] - b[1])
	p = (aa + bb + cc) / 2
	s = (p * (p - aa) * (p - cc) * (p - bb)) ** 0.5
	h = 2 * s / cc
	if h > r:
		return False
	else:
		return True


thread1 = threading.Thread(target=getblue0)
thread1.start()
i = len(path) - 1
goal = np.array([path[i][0], path[i][1]])
k = -1
GOAL_FLAG=True
# 4. 主循环
while True:
	# 4.1 根据DWA计算所应该施加的控制指令
	# u[0]是机器人x轴速度，u[1]是机器人y轴速度
	angle = togoal(blue[0], goal)
	ro_b_0.setSpeed(speed * np.sin(angle), speed * np.cos(angle), 0)
	# u, ltraj = dwa_control(x, u, config, goal, ob, ro_b_0, camera)
	# print(u)
	# if np.hypot(traj[-1,0]-traj[0,0],traj[-1,1]-traj[0,1]) <0.1:
	# 	pf = statics_map([blue[0].x, blue[0].y], end_point, blue, yellow, radius)
	# 	pf.shorter_the_path(2, 10)
	# 	path = pf.get_path()
	distance = math.sqrt((blue[0].x - goal[0]) ** 2 + (blue[0].y - goal[1]) ** 2)
	if distance <= 1:
		speed = 0.2 + 2.3 * distance
		if distance <= 0.1:
			if i == 0:
				k = 1
				GOAL_FLAG=True
			if i == len(path) - 1:
				k = -1
				GOAL_FLAG=False
			i = i + k
			goal = np.array([path[i][0], path[i][1]])
			speed = 2.5


	# if (np.hypot(ltraj[-1][0] - ltraj[0][0], ltraj[-1][1] - ltraj[0][1])) <0.1:
	# 	if i > 1 or i < len(path)-2:
	# 		config.to_goal_cost_gain+=1
	debug = DBG()
	debug.addPath_rrt(path, 4)  # 将路径画出来
	# debug.addpath_dwa(ltraj)
	debug.sendDebugMessage()  # debug信息发送
# time.sleep(0.015)
# chase2(blue[0],[path_x,path_y],ro_b_0,1,1)
