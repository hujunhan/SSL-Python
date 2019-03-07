import time
import socket
import sys
from SSL_Lib import vision_detection_pb2
from SSL_Lib.Robot import *

#初始化控制和读取的IP地址、端口号
control_addr = ('127.0.0.1', 20011)
read_addr = ('127.0.0.1', 23334)
control_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
read_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM,0)
read_socket.bind(read_addr)

vision_frame=vision_detection_pb2.Vision_DetectionFrame()

vision_data=read_socket.recv(4096)#读取信息
vision_frame.ParseFromString(vision_data)#解析数据
ro_blue=vision_frame.robots_blue  #读取数据中蓝色机器人的数据

ro_b_3 = Robot("blue", 5)
ro_b_3.setSpeed(0, 1, 0)
while True:
    control_socket.sendto(ro_b_3.getSpeedCommand(),control_addr)
    print(getPos("blue",6,read_socket))
    
control_socket.close()
