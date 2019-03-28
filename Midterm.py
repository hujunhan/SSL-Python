from SSL_Lib.Robot import Robot
from SSL_Lib.Camera import Camera
from SSL_Lib.DStar import DStar
import matplotlib.pyplot as plt

read_addr = ('127.0.0.1', 23333)
camera = Camera(read_addr)
# 定义我们自己的小车
player = Robot('blue', 0, 0.15, 'COM5')

pf = DStar(x_start=-40, y_start=0, x_goal=0, y_goal=0)  # 初始化
pf.initialize_map(120,90)
plt.grid(True)
# while True:
# plt.clf()
# blue, yellow = camera.getRobotDict()
# for ro in blue.values():
# 	if ro.robot_id is not 0:
# 		pass
# 		pf.set_obstract(int(ro.x / 100), int(ro.y / 100), 5)
# 		plt.plot(int(ro.x / 100), int(ro.y / 100), 'ob', ms=10)
pf.set_obstract(-35,0,4)
pf.set_obstract(-25,0,4)
pf.set_obstract(-15,0,4)
pf.set_obstract(-5,0,4)
pf.replan()
path = pf.get_path()
print(path)
x=[]
y=[]
for s in path:
	x.append(s.x)
	y.append(s.y)
plt.plot(x,y)
	#plt.plot(s.x,s.y,'')
plt.show()
