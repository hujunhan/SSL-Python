from SSL_Lib.DStar import DStar
import matplotlib.pyplot as plt
import random
import numpy as np


###
def draw():
	plt.clf()
	for _ in range(10):
		x = int(random.random() * 120)
		y = int(random.random() * 90)
		plt.plot(x,y,'ob',ms=15)

pf.initialize_map(120, 90)
pf = DStar(x_start=60, y_start=60, x_goal=5, y_goal=5)  # 初始化

for _ in range(10):
	x = int(random.random() * 120)
	y = int(random.random() * 90)
	pf.set_obstract(x, y, 1)

pf.set_obstract(2, 2, 3)  # 设置障碍物位置和大小，默认圆形
pf.replan()  # 路径规划
plan = pf.get_path()  # 内为当前路径
# print(plan[0])
# plan[1].y #内为第i步位置
draw()
plt.grid(True)
plt.show()
