from SSL_Lib.Robot import Robot
from SSL_Lib.Camera import Camera
from SSL_Lib.DStar import DStar
from SSL_Lib.P2P import P2P
import matplotlib.pyplot as plt
import serial
import time
FIRST_CONNETION=False
serialPort="COM3"   #串口
baudRate=115200      #波特率
start_package = b'\xff\xb0\x01\x02\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x31'
config_package= b'\xff\xb0\x04\x05\x06\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x85'#频点为0
read_addr = ('127.0.0.1', 23333)
camera = Camera(read_addr)
# 定义我们自己的小车
player = Robot('blue', 0, 0.15, 'COM5')


ser=serial.Serial(serialPort,baudRate,timeout=0.5)
print('serial port open: ',ser.isOpen())
print ("参数设置：串口=%s ，波特率=%d"%(serialPort,baudRate))
if FIRST_CONNETION:
	while True:
		a=ser.write(start_package)
		a=ser.readline()
		if a is not b'':
			print('Start package has been sent!')
			break
	ser.write(config_package)

def statics_map():
	pf = DStar(x_start=-50, y_start=-5, x_goal=58, y_goal=10)  # 初始化
	pf.initialize_map(120, 90)
	blue, yellow = camera.getRobotDict()
	for ro in blue.values():
		if ro.robot_id is not 0:
			pf.set_obstract(int(ro.x / 100), int(ro.y / 100), 5)
			plt.plot(int(ro.x / 100), int(ro.y / 100), 'ob', ms=5)

	for ro in yellow.values():
		if ro.robot_id is not 0:
			pf.set_obstract(int(ro.x / 100), int(ro.y / 100), 5)
			plt.plot(int(ro.x / 100), int(ro.y / 100), 'oy', ms=5)

	pf.replan()
	path = pf.get_path()
	return path
plt.ion()
plt.grid(True)
#主逻辑
i=0
ro_b_0=Robot('blue',0,0.15,'COM')
while True:
	plt.clf()
	
	path=statics_map()
	path_x=path[i].x
	path_y=path[i].y
	xx,yy,success,vx,vy = P2P(ro_b_0,camera,path_x,path_y)
	if success is 1:
		i=i+1
	x = []
	y = []
	for s in path:
		x.append(s.x)
		y.append(s.y)
	plt.plot(x, y)
	# plt.plot(s.x,s.y,'')
	plt.show()
	plt.close()
