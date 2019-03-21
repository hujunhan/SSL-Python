import time
import socket
import sys
from SSL_Lib import vision_detection_pb2
from SSL_Lib.Robot import *
from SSL_Lib.Camera import *
from SSL_Lib.P2P import *
# 初始化控制和读取的IP地址、端口号
control_addr = ('127.0.0.1', 20011)
read_addr = ('127.0.0.1', 23334)

ro_b_0 = Robot("blue", 0,0.15,control_addr)

camera=Camera(read_addr)
x,y,ori=camera.getRobotPos()

#ro_b_0.setSpeed(0, 1, 0)  # 设置要测试的命令
time_start = time.time()  # 记录测试开始的时间
x, y, ori = camera.getRobotPos()
dest_x=3
dest_y=4
vy=0
vx=0
distance0=((x[0]-dest_x)**2+(y[0]-dest_y)**2)**0.5
ay=(dest_x-x[0])/distance0/20
ax=(dest_y-y[0])/distance0/20
while True:
    #print(getXY("blue",0,read_socket))
    
    x, y, ori = camera.getRobotPos()
    distance=((x[0]-dest_x)**2+(y[0]-dest_y)**2)**0.5
    w=0
    if(distance>0.5*distance0):
        if vx<2 and vy<2:
            vx=vx+ax
            vy=vy+ay
    else:
        if vx>0 and vy>0:
            vx=vx-ax
            vy=vy-ay
    ro_b_0.setSpeed(vx,vy,w)
    print("vx=",vx,"vy=",vy,"w=",w)
    print("x=",x[0],"y=",y[0],"distance=",distance)
    if distance<0.1:
        print("Success!")
        ro_b_0.setSpeed(0,0,0)
        break
    # if(ori[0] > 3.14/2):  # 设置判断规则，可以是角度啊，位置啥的
    #     time_stop = time.time()  # 记录测试结束的时间
    #     ro_b_0.setSpeed(0, 0, 0)  # 把机器人停下来
    #     x, y, ori = camera.getRobotPos()
    #     print('total time is ', time_stop-time_start)  # 打印出来所用的时间
    #     print('now ori is ', ori[0])  # 打印出来要测试的信息
    #     break
    # else:
    #     pass

