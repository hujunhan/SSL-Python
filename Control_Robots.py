import time
import socket
import sys
from SSL_Lib import vision_detection_pb2
from SSL_Lib.Robot import *
from SSL_Lib.Camera import *
# 初始化控制和读取的IP地址、端口号
control_addr = ('127.0.0.1', 20011)
read_addr = ('127.0.0.1', 23334)

ro_b_0 = Robot("blue", 0,control_addr)
camera=Camera(read_addr)

ro_b_0.setSpeed(0, 1, 1)  # 设置要测试的命令
time_start = time.time()  # 记录测试开始的时间

while True:
    # control_socket.sendto(ro_b_0.getSpeedCommand(),control_addr)
    # print(getXY("blue",0,read_socket))
    x, y, ori = camera.getRobotPos()
    if(ori[0] > 3.14/2):  # 设置判断规则，可以是角度啊，位置啥的
        time_stop = time.time()  # 记录测试结束的时间
        ro_b_0.setSpeed(0, 0, 0)  # 把机器人停下来
        x, y, ori = camera.getRobotPos()
        print('total time is ', time_stop-time_start)  # 打印出来所用的时间
        print('now ori is ', ori[0])  # 打印出来要测试的信息
        break
    else:
        pass

