import time
import socket
import random
import sys
import numpy as np
from SSL_Lib import vision_detection_pb2
from SSL_Lib.Robot import *
from SSL_Lib.Camera import *
from SSL_Lib.utils import *
# 初始化控制和读取的IP地址、端口号
control_addr = ('127.0.0.1', 20011)
read_addr = ('127.0.0.1', 23333)


def chase(robot, goal):
    for ro in robot:
        if ro.id in blue:
            if goal.id in blue:
                angle = calc_angle(blue[ro.id], blue[goal.id])
                ro.setSpeed(0, 1, -angle+np.random.uniform(-0.1,0.1))


def random_robot(robot):
    for ro in robot:
        ro.setSpeed(0, 1, random.random())


ob0 = Robot("blue", 0, 0.15, control_addr)
ob2 = Robot("blue", 2, 0.15, control_addr)
ob3 = Robot("blue", 3, 0.15, control_addr)
goal = Robot("blue", 1, 0.15, control_addr)
obstacle = [ob0, ob2, ob3]
camera = Camera(read_addr)
while True:
    blue, yellow = camera.getRobotDict()
    chase(obstacle, goal)
