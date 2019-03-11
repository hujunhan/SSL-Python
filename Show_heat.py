import time
import socket
import sys
from SSL_Lib import vision_detection_pb2
from SSL_Lib.Robot import *
from SSL_Lib.APF import *
from SSL_Lib.Camera import *
# 初始化控制和读取的IP地址、端口号
control_addr = ('127.0.0.1', 20011)
read_addr = ('127.0.0.1', 23334)
camera=Camera(read_addr)
ox,oy,oz=camera.getRobotPos()
a=plot_heat(ox,oy)
plt.show(a)
