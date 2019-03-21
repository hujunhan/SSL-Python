import time
import socket
import sys
from SSL_Lib import vision_detection_pb2
from SSL_Lib.Robot import Robot
from SSL_Lib.APF import plot_heat
from SSL_Lib.Camera import Camera
import matplotlib.pyplot as plt
# 初始化控制和读取的IP地址、端口号
control_addr = ('127.0.0.1', 20011)
read_addr = ('127.0.0.1', 23334)
camera=Camera(read_addr)
b,y=camera.getRobotDict()
print(y.values())
