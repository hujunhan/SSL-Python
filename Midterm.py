import socket

from SSL_Lib.Robot import Robot
from SSL_Lib.Camera import Camera
from SSL_Lib.DStar import DStar
from SSL_Lib.utils import *
from SSL_Lib.DBG import DBG
import serial
import sys
import time
FIRST_CONNECTION=False
serialPort = "COM3"  # 串口
# 初始化控制和读取的IP地址、端口号
control_addr = ('127.0.0.1', 20011)
read_addr = ('127.0.0.1', 23333)
camera = Camera(read_addr)
debug = DBG()

#ser = serial.Serial(serialPort, 115200, timeout=0.5)
if FIRST_CONNECTION:
	config_serial(serialPort)


# 主逻辑

#1.初始化要控制的机器人
ro_b_0 = Robot('blue', 0, 0.15, control_addr=control_addr)
blue, yellow = camera.getRobotDict()  # 读取初始信息
start_point = [blue[0].x, blue[0].y]  # 设置机器人开始的位置
end_point = [-start_point[0], -start_point[1]]  # 设置机器人终点为对称点
print(start_point)
#2.目前只测试静态避障，所以只生成一次路径规划
path = statics_map(start_point,end_point,camera) #从Dstar获取路径信息
path=path[::10]
print(path)
debug.addPath(path) #将路径画出来
debug.sendDebugMessage() #debug信息发送
i = 0
goal_point=[path[-1].x,path[-1].y]
while True:
	blue, yellow = camera.getRobotDict()
	path_x = path[i].x
	path_y = path[i].y
	point_dis = calc_distance(blue[0], [path_x, path_y])
	goal_dis=calc_distance(blue[0],goal_point)
	if point_dis < 2:
		i = i + 1
		if i is len(path):##回到起始点
			ro_b_0.setSpeed(0, 0, 0)
			a=input('Type anything to go back or type q to break ') #随便打点什么
			if a is 'q':
				break
			blue, yellow = camera.getRobotDict()  # 读取初始信息
			start_point = [blue[0].x, blue[0].y]  # 设置机器人开始的位置
			end_point = [start_point[1], start_point[0]]  # 设置机器人终点为对称点
			path = statics_map(start_point, end_point, camera)  # 从Dstar获取路径信息
			debug=DBG()
			debug.addPath(path)
			debug.sendDebugMessage()
			i=0
			ro_b_0.setSpeed(0,0,1)
			time.sleep(3)
			ro_b_0.setSpeed(0,0,0)
			continue
		continue
	chase(blue[0], [path_x, path_y],ro_b_0) ##最最简单的路径跟踪
