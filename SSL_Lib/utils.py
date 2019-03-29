import numpy as np
from SSL_Lib.DStar import DStar
from SSL_Lib.Camera import Camera
import serial


def calc_angle(start, goal):
	# 起始点的信息
	start_x = start.x
	start_y = start.y
	start_ori = start.orientation

	# 终点的信息
	goal_x = goal[0] * 100
	goal_y = goal[1] * 100

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
	return np.hypot(goal[1] - start.y / 100, goal[0] - start.x / 100)


def statics_map(start_point, end_point, camera):
	x_start = int(start_point[0] / 100)
	y_start = int(start_point[1] / 100)
	x_goal = int(end_point[0] / 100)
	y_goal = int(end_point[1] / 100)
	pf = DStar(x_start, y_start, x_goal, y_goal)  # 初始化
	pf.initialize_map(120, 90)
	blue, yellow = camera.getRobotDict()
	for ro in blue.values():
		if ro.robot_id is not 0:
			pf.set_obstract(int(ro.x / 100), int(ro.y / 100), 3)

	for ro in yellow.values():
		pf.set_obstract(int(ro.x / 100), int(ro.y / 100), 3)

	pf.replan()
	path = pf.get_path()
	return path


##最最简单的路径跟踪
def chase(robot, goal, control_robot,speed,point_dis):
	t=point_dis/speed
	angle = calc_angle(robot, goal)
	a = control_robot.setSpeed(0, speed, -angle*2)


def config_serial(serialPort):
	baudRate = 115200  # 波特率
	start_package = b'\xff\xb0\x01\x02\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x31'
	config_package = b'\xff\xb0\x04\x05\x06\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x85'  # 频点为0
	ser = serial.Serial(serialPort, baudRate, timeout=0.5)

	while True:
		a = ser.write(start_package)
		a = ser.readline()
		if a is not b'':
			print('Start package has been sent!')
			break
	ser.write(config_package)