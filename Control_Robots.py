import time
import socket
import sys
from SSL_Lib import vision_detection_pb2
import numpy as np
from SSL_Lib.Robot import *
from SSL_Lib.Camera import *
from SSL_Lib.P2P import *
# 初始化控制和读取的IP地址、端口号
control_addr = ('127.0.0.2', 20011)
read_addr = ('127.0.0.1', 23334)

ro_b_0 = Robot("blue", 0,0.15,control_addr)

camera=Camera(read_addr)
success=0
#ro_b_0.setSpeed(0, 1, 0)  # 设置要测试的命令
time_start = time.time()  # 记录测试开始的时间

xx,yy,success = P2P(ro_b_0,camera,1,1)
x,y,ori=camera.getRobotPos()
print("success=",success,"x=",x[0],"y=",y[0])
if success is not -1:
    xx,yy,success = P2P(ro_b_0,camera,1.2,1.8)
    x,y,ori=camera.getRobotPos()
    print("success=",success,"x=",x[0],"y=",y[0])
if success is not -1:
    xx,yy,success = P2P(ro_b_0,camera,2.1,3.6)
    x,y,ori=camera.getRobotPos()
    print("success=",success,"x=",x[0],"y=",y[0])
if success is not -1:
    xx,yy,success = P2P(ro_b_0,camera,2.5,-2)
    x,y,ori=camera.getRobotPos()
    print("success=",success,"x=",x[0],"y=",y[0])
    # if(ori[0] > 3.14/2):  # 设置判断规则，可以是角度啊，位置啥的
    #     time_stop = time.time()  # 记录测试结束的时间
    #     ro_b_0.setSpeed(0, 0, 0)  # 把机器人停下来
    #     x, y, ori = camera.getRobotPos()
    #     print('total time is ', time_stop-time_start)  # 打印出来所用的时间
    #     print('now ori is ', ori[0])  # 打印出来要测试的信息
    #     break
    # else:
    #     pass

