import socket

from SSL_Lib.Robot import Robot
from SSL_Lib.Camera import Camera
from SSL_Lib.DStar import DStar
from SSL_Lib.utils import *
from SSL_Lib.DBG import DBG
import serial
import sys
import time

serialPort = "COM4"  # 串口
# 初始化控制和读取的IP地址、端口号
localhost = '127.0.0.1'
control_addr = (localhost, 20011)
read_addr = (localhost, 23333)
camera = Camera(read_addr)
debug = DBG()
# ser=None
ser = serial.Serial(serialPort, 115200, timeout=0.5)
# ser=config_serial(serialPort)
# 主逻辑


# 1.初始化要控制的机器人
blue, yellow = camera.getRobotDict()  # 读取初始信息

ro_b_0 = Robot('blue', 0, 0.15, ser=ser, control_addr=control_addr)

start_point = [blue[0].x, blue[0].y]  # 设置机器人开始的位置
end_point = [-start_point[0], -start_point[1]]  # 设置机器人终点为对称点
print('start at: ', start_point)
print('goal at: ', end_point)

# 2.目前只测试静态避障，所以只生成一次路径规划
radius = 20
path = statics_map(start_point, end_point, camera, radius)  # 从Dstar获取路径信息
while path is None:  # 如果障碍物膨胀太多，就逐渐减小
	radius = radius - 1
	if radius < 5:
		print('No way out!')
		break
	print('Now trying radius = ', radius)
	path = statics_map(start_point, end_point, camera, radius)

print('get path!')
print('path start at: ', path[0])
print('path end at: ', path[-1])

print('length of path: ', len(path))
path = path[::100]
print('length of path(reduced): ', len(path))
debug.addPath(path)  # 将路径画出来
debug.sendDebugMessage()  # debug信息发送
i = 1
speed = 1

# 3. 调整角度，使机器人指向指定点
point = (path[i].x, path[i].y)
angle = calc_angle(blue[0], (path[i].x, path[i].y))
point_at(ro_b_0, point, camera, np.pi / 200)

# 4. 主循环
while True:
	# 4.1 更新一下位置
	blue, yellow = camera.getRobotDict()
	path_x = path[i].x
	path_y = path[i].y
	point_dis = calc_distance(blue[0], [path_x, path_y])
	angle = calc_angle(blue[0], (path[i].x, path[i].y))
	print(angle)
	# 4.2 根据位置设置速度，从50cm处开始减速
	speed = 1 * (1 - 2 * abs(angle) / np.pi)
	print(speed)
	if point_dis < 50:
		speed = 0.02 * point_dis
	# 4.3 如果距离小于5cm，认为已经达到这个点，开始走下一个点
	if point_dis < 10:
		i = i + 1

		if i is len(path):  ## 4.3.1 如果到终点了，则重新规划，要么结束程序，要么走向对称点
			print('Now the robot is near the goal!')
			ro_b_0.setSpeed(0, 0, 0)
			a = input('Type anything to go back or type q to break ')  # 随便打点什么
			print(a)
			if a is 'q':
				break
			else:
				blue, yellow = camera.getRobotDict()  # 读取初始信息
				start_point = [blue[0].x, blue[0].y]  # 设置机器人开始的位置
				end_point = [-start_point[0], -start_point[1]]  # 设置机器人终点为对称点
				path = statics_map(start_point, end_point, camera, radius)  # 从Dstar获取路径信息
				path = path[::100]
				debug = DBG()
				debug.addPath(path)
				debug.sendDebugMessage()
				i = 1  # 指向第一个点
				point_at(ro_b_0, (path[i].x, path[i].y), camera, np.pi / 20)
				angle = calc_angle(blue[0], (path[i].x, path[i].y))
				print(angle)
				speed = 1 * (1 - abs(angle) / np.pi)
				# ro_b_0.setSpeed(0, 0, 0)
				continue
		if angle > np.pi / 6:
			point_at(ro_b_0, (path[i].x, path[i].y), camera, np.pi / 200)
		continue

	chase(blue[0], [path_x, path_y], ro_b_0, speed, point_dis, camera)  ##最最简单的路径跟踪
# chase2(blue[0],[path_x,path_y],ro_b_0,1,1)
