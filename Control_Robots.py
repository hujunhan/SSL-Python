import time
import socket
import sys
from SSL_Lib import vision_detection_pb2
from SSL_Lib.Robot import *

# 初始化控制和读取的IP地址、端口号
control_addr = ('127.0.0.1', 20011)
read_addr = ('127.0.0.1', 23334)
control_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
read_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
read_socket.bind(read_addr)

vision_frame = vision_detection_pb2.Vision_DetectionFrame()

ro_b_0 = Robot("blue", 0)
ro_b_0.setReplacement(0, 0, 0)  # 将机器人移动到中心点
control_socket.sendto(ro_b_0.getSpeedCommand(), control_addr)
for _ in range(10):  # 信号读取会有几帧的延迟，所以要将可能是缓存的位置读掉
    x, y, ori = getXYA("blue", 0, read_socket)  # 否则会出现读取错位的问题
ro_b_0.clearCommand()  # 清空一下命令
ro_b_0.setSpeed(0, 1, 1) #设置要测试的命令
control_socket.sendto(ro_b_0.getSpeedCommand(), control_addr)
time_start = time.time() #记录测试开始的时间

while True:
    # control_socket.sendto(ro_b_0.getSpeedCommand(),control_addr)
    # print(getXY("blue",0,read_socket))
    x, y, ori = getXYA("blue", 0, read_socket)
    if(ori > 3.14/2): #设置判断规则，可以是角度啊，位置啥的
        time_stop = time.time() #记录测试结束的时间
        ro_b_0.setSpeed(0, 0, 0) #把机器人停下来
        control_socket.sendto(ro_b_0.getSpeedCommand(), control_addr)
        x, y, ori = getXYA("blue", 0, read_socket)
        print('total time is ', time_stop-time_start) #打印出来所用的时间
        print('now ori is ', ori) #打印出来要测试的信息
        break
    else:
        pass
control_socket.close()
read_socket.close()
