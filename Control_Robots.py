import time
import socket
import sys
from SSL_Lib import vision_detection_pb2
import numpy as np
from SSL_Lib.Robot import *
from SSL_Lib.Camera import *
from SSL_Lib.P2P import *
import matplotlib.pyplot as plt
from SSL_Lib.DStar import DStar
import numpy as np
# 初始化控制和读取的IP地址、端口号
control_addr = ('127.0.0.2', 20011)
read_addr = ('127.0.0.1', 23334)

ro_b_0 = Robot("blue", 0,0.15,control_addr)
camera=Camera(read_addr)

x,y,ori=camera.getRobotPos()
goal=[10,10]
pf = DStar(x_start=int(-400), y_start=int(0), x_goal=goal[0], y_goal=goal[1])
for i in range(1,13):
    pf.set_obstract(round(x[i]*100),round(y[i]*100),15)
pf.replan()
##至此 静态路径规划完成
print(len(pf.path))
print(pf.path)
while True:

    success=0
#time_start = time.time()  # 记录测试开始的时间
for index in range(len(pf.path)-1):
    xx,yy,success = P2P(ro_b_0,camera,pf.path[index].x/100,pf.path[index].y/100)
    print("index=",index,"success=",success,"nowx=",x[0],"nowy=",y[0],"wantx=",pf.path[index].x/100,"wanty=",pf.path[index].y/100)
