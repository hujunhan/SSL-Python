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

serialPort = "COM5"  # 串口
# 初始化控制和读取的IP地址、端口号
localhost = '127.0.0.1'
control_addr = (localhost, 20011)
read_addr = (localhost, 23333)
camera = Camera(read_addr)
debug = DBG()
ser = None
# ser = serial.Serial(serialPort, 115200, timeout=0.5)
# ser=config_serial(serialPort)
# 主逻辑

radius = 0.5
# 1.初始化要控制的机器人
ro_b_0 = Robot('yellow', 0, 0.15, control_addr=control_addr, ser=ser)

blue, yellow = camera.getRobotDict()  # 读取初始信息
start_point = [yellow[0].x, yellow[0].y]  # 设置机器人开始的位置
end_point = [-start_point[0], -start_point[1]]  # 设置机器人终点为对称点
A_point = [-2.5, 1.5]
B_point = [2.5, -1.5]
# end_point = [-2.5, 1.5]  # 设置机器人终点为对称点
print('start at: ', start_point)
print('goal at: ', end_point)

# 2.目前只测试静态避障，所以只生成一次路径规划
ob_temp = []
for ro in yellow.values():
	if ro.robot_id is not 0:
		ob_temp.append((ro.x, ro.y, radius))
for ro in blue.values():
	ob_temp.append((ro.x, ro.y, radius))
ob = np.array(ob_temp)
print('ob = ', ob_temp)
u = np.array([0.0, 0.0])
config = Config()
# 2.1 新建地图
starttime = time.time()
rrt = RRT(start=[yellow[0].x, yellow[0].y], goal=A_point,
		  randArea=[5, 3.6], obstacleList=ob)
path = rrt.Planning(animation=False)
maxIter = 4000
path = PathSmoothing(path, maxIter, ob_temp)
print('Using ', time.time() - starttime, ' to calculate rrt!')
x = np.array([yellow[0].x, yellow[0].y, yellow[0].orientation, 0.0, 0.0])
traj = np.array(x)

print(path)
goal = np.array([path[0][0], path[0][1]])

print('get path!')
print('path start at: ', path[0])
print('path end at: ', path[-1])
print('length of path: ', len(path))
print('length of path(reduced): ', len(path))

i = 0
speed = 2.5


# 3. 新建一个进程
# 用来另开一个线程的函数
def getblue0():
	global blue, yellow, ob
	while True:
		blue, yellow = camera.getRobotDict()
		ob_temp1 = []
		for ro in blue.values():
			ob_temp1.append([ro.x, ro.y, radius])
		for ro in yellow.values():
			if ro.robot_id is not 0:
				ob_temp1.append(([ro.x, ro.y, radius]))
		ob = np.array(ob_temp1)


def checkDanger():
	sx = yellow[0].x
	sy = yellow[0].y
	gx = goal[0]
	gy = goal[1]
	for ro in ob:
		if ((ro[0] - sx) * (ro[0] - gx)) < 0:
			if ((ro[1] - sy) * (ro[1] - gy)) < 0:
				if checkInLine([sx, sy], [gx, gy], [ro[0], ro[1]], radius):
					return True


thread1 = threading.Thread(target=getblue0)
thread1.start()
i = len(path) - 1
goal = np.array([path[i][0], path[i][1]])
k = -1
GOAL_FLAG = False
# 4. 主循环
while True:
	# 实际地图500*360
	if checkDanger():
		print('danger!')
		angle = togoal(yellow[0], goal)
		ro_b_0.setSpeed(0.2 * speed * np.sin(angle), 0.2 * speed * np.cos(angle), 0)
		GOAL_FLAG = ~GOAL_FLAG
		if GOAL_FLAG:
			xx = A_point
		else:
			xx = B_point
		GOAL_FLAG = ~GOAL_FLAG
		rrt = RRT(start=[yellow[0].x, yellow[0].y], goal=xx,
				  randArea=[5, 3.6], obstacleList=ob)
		path = rrt.Planning(animation=False)
		maxIter = 4000
		path = PathSmoothing(path, maxIter, ob_temp)
		i = len(path) - 1
		goal = np.array([path[i][0], path[i][1]])
		k = -1
		time.sleep(0.003)

	angle = togoal(yellow[0], goal)
	ro_b_0.setSpeed(speed * np.sin(angle), speed * np.cos(angle), 0)
	distance = math.sqrt((yellow[0].x - goal[0]) ** 2 + (yellow[0].y - goal[1]) ** 2)
	if distance <= 1:
		speed = 1.5 + 1 * distance
		if distance <= 0.1:
			if i == 0:
				if GOAL_FLAG:
					xx = A_point
				else:
					xx = B_point
				rrt = RRT(start=[yellow[0].x, yellow[0].y], goal=xx,
						  randArea=[5, 3.6], obstacleList=ob)
				path = rrt.Planning(animation=False)
				maxIter = 1000
				path = PathSmoothing(path, maxIter, ob_temp)
				i = len(path) - 1
				GOAL_FLAG = ~GOAL_FLAG
			i = i + k
			goal = np.array([path[i][0], path[i][1]])
			speed = 2.5

	debug = DBG()
	debug.addPath_rrt(path, 4)  # 将路径画出来
	# debug.addpath_dwa(ltraj)
	# debug.addSide()
	debug.sendDebugMessage()  # debug信息发送
