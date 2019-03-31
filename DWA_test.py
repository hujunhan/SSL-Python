import time
import socket
import sys
from SSL_Lib import vision_detection_pb2
from SSL_Lib.Robot import *
from SSL_Lib.Camera import *
from SSL_Lib.P2P import *
from SSL_Lib.DWA import *
from SSL_Lib.DStar import *
from SSL_Lib.DBG import DBG
# 初始化控制和读取的IP地址、端口号
control_addr = ('127.0.0.1', 20011)
read_addr = ('127.0.0.1', 23334)

ro_b_0 = Robot("blue", 0,0.15,control_addr)
debug=DBG()
camera=Camera(read_addr)

blue,yellow=camera.getRobotDict()

print(blue[0])
x = np.array([blue[0].x/1000, blue[0].y/1000, blue[0].orientation, 0.0, 0.0])
goal=np.array([blue[0].x/1000+1,blue[0].y/1000+1])

print('start at ',x)
print('goal is ',goal)
ro_b_0=Robot('blue',0,0.15,control_addr)
ob=[]
for ro in blue.values():
	if ro.robot_id is not 0:
		ob.append([ro.x/1000,ro.y/1000])
for ro in yellow.values():
	ob.append(([ro.x/1000,ro.y/1000]))
obnp=np.array(ob)


u=np.array([0.0,0.0])
config=Config()

traj=np.array(x)
while True:
	u, ltraj = dwa_control(x, u, config, goal, obnp,ro_b_0,camera)
	print('u is ',u)
	#a=input('??????????')
	x=sim_motion(ro_b_0,u,camera)
	if math.sqrt((x[0] - goal[0]) ** 2 + (x[1] - goal[1]) ** 2) <= config.robot_radius:
		print("Goal!!")
		break
	debug=DBG()
	debug.addpath_dwa(ltraj)
	debug.sendDebugMessage()
	time.sleep(0.01)

