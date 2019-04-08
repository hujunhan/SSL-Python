import time
import socket
import sys
import threading
from SSL_Lib import vision_detection_pb2
from SSL_Lib.Robot import *
from SSL_Lib.Camera import *
from SSL_Lib.P2P import *
from SSL_Lib.DWA1 import *
from SSL_Lib.DStar import *
from SSL_Lib.DBG import DBG
import matplotlib.pyplot as plt
from SSL_Lib.utils import*

# 初始化控制和读取的IP地址、端口号
show_animation = True
control_addr = ('127.0.0.1', 20011)
read_addr = ('127.0.0.1', 23334)

# 初始化机器人，DEBUG和camera实例
ro_b_0 = Robot("blue", 0, 0.15, control_addr)
debug = DBG()
camera = Camera(read_addr)

# 初始化起点，并自定义终点
blue, yellow = camera.getRobotDict()
x = np.array([blue[0].x / 1000, blue[0].y / 1000, blue[0].orientation, 0.0, 0.0])
goal = np.array([-blue[0].x / 1000, -blue[0].y / 1000])
print('start at ', x)
print('goal is ', goal)


# 用来另开一个线程的函数
def getblue0():
	global blue
	while True:
		x, y = camera.getRobotDict()
		blue[0] = x[0]


thread1 = threading.Thread(target=getblue0)
thread1.start()



# 用来初始化控制信号和配置信息
u = np.array([0.0, 0.0])
config = Config()
traj = np.array(x)

# thread1.setDaemon(True)
while True:
	angle=togoal(blue[0],[0,0])
	ro_b_0.setSpeed(2*np.sin(angle),2*np.cos(angle),0)
	debug = DBG()
	debug.addText(10,10,str(angle))
	debug.sendDebugMessage()
