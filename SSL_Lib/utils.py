import numpy as np
from SSL_Lib.DStar import DStar
from SSL_Lib.Camera import Camera
import serial
import threading
import time

def getx(camera):
	blue,yellow=camera.getRobotDict()
	return blue[0]

def calc_angle(start, goal):
	# 起始点的信息
	start_x = start.x
	start_y = start.y
	start_ori = start.orientation

	# 终点的信息
	goal_x = goal[0] * 10
	goal_y = goal[1] * 10

	# 起点指向终点的角度
	vector_angle = np.arctan2(goal_y - start_y, goal_x - start_x)
	# print(vector_angle)
	# 要返回的angle，但是范围有可能超出-pi-pi
	angle = start_ori - vector_angle
	if (angle > np.pi):
		angle = angle - np.pi * 2
	if (angle < -np.pi):
		angle = angle + np.pi * 2
	return angle


def calc_distance(start, goal):
	return np.hypot(goal[1] - start.y / 10, goal[0] - start.x / 10)


# 地图大小5mx3.6m
def statics_map(start_point, end_point, blue,yellow, radius):
	x_start = int(start_point[0] / 10)
	y_start = int(start_point[1] / 10)
	x_goal = int(end_point[0] / 10)
	y_goal = int(end_point[1] / 10)
	pf = DStar(x_start, y_start, x_goal, y_goal)  # 初始化
	pf.initialize_map(1200, 900)
	for ro in blue.values():
		if ro.robot_id is not 0:
			pf.set_obstract(int(ro.x / 10), int(ro.y / 10), radius,-1)
	for ro in yellow.values():
		pf.set_obstract(int(ro.x / 10), int(ro.y / 10), radius,-1)

	pf.replan()
	pf.shorter_the_path(1)
	path = pf.get_path()
	return path


##最最简单的路径跟踪
def chase(robot, goal, control_robot, speed, point_dis, camera):
	t = point_dis / speed
	angle = calc_angle(robot, goal)
	# if abs(angle) > np.pi / 6:
	# 	while abs(angle) > np.pi / 12:
	# 		blue, yellow = camera.getRobotDict()
	# 		angle = calc_angle(blue[0], goal)
	# 		speeda = speed * (90 - abs(angle) * 90 / np.pi) / 90
	# 		control_robot.setSpeed(0, 0, angle)
	a = control_robot.setSpeed(0, speed, 2*angle)


def chase2(robot, goal, control_robot, speed, point_dis):
	angle = calc_angle(robot, goal)
	vx = speed * np.cos(angle)
	vy = speed * np.sin(angle)
	control_robot.setSpeed(vx, vy, 0)


def config_serial(serialPort):
	baudRate = 115200  # 波特率
	start_package = b'\xff\xb0\x01\x02\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x31'
	config_package = b'\xff\xb0\x04\x05\x06\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x85'  # 频点为0
	ser = serial.Serial(serialPort, baudRate, timeout=0.5)
	a = ser.write(start_package)
	a = ser.readline()
	while not a:
		a = ser.write(start_package)
		a = ser.readline()
	print(a)
	b = ser.write(config_package)

	return ser


def point_at(robot, point, camera, tolerance):
	print('start spin')
	blue, yellow = camera.getRobotDict()
	angle = calc_angle(blue[0], point)
	if abs(angle) > tolerance:
		while abs(angle) > np.pi / 200:
			robot.setSpeed(0, 0, 1 if angle > 0 else -1)
			blue, yellow = camera.getRobotDict()
			angle = calc_angle(blue[0], point)
