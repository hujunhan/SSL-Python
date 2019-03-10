import time
import socket
import sys
from SSL_Lib import vision_detection_pb2
from SSL_Lib.Robot import *
from SSL_Lib.APF import *
# 初始化控制和读取的IP地址、端口号
control_addr = ('127.0.0.1', 20011)
read_addr = ('127.0.0.1', 23334)
control_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
read_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
read_socket.bind(read_addr)
vision_frame = vision_detection_pb2.Vision_DetectionFrame()
while True:
    ox,oy=getObstacleXY(read_socket)
    print(ox)
    a=plot_heat(ox,oy)
    plt.show(a)
    plt.close()
