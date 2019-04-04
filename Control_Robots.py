import time
import socket
import sys
from SSL_Lib import vision_detection_pb2
from SSL_Lib.Robot import *
from SSL_Lib.Camera import *
from SSL_Lib.P2P import *
from SSL_Lib.DStar import *
# 初始化控制和读取的IP地址、端口号
control_addr = ('127.0.0.1', 20011)
read_addr = ('127.0.0.1', 23334)

ro_b_0 = Robot("blue", 0,0.15,control_addr)
ro_b_0.sim = True

camera=Camera(read_addr)
x,y,ori=camera.getRobotPos()

#ro_b_0.setSpeed(0, 1, 0)  # 设置要测试的命令
time_start = time.time()  # 记录测试开始的时间
x, y, ori = camera.getRobotPos()
dest_x,dest_y=0,0
vx,vy=0,0

pf = DStar((int)(x[0]*100), (int)(y[0]*100), dest_x, dest_y)
pf = DStar(-400,0, 0, 0)
pf.set_obstract(-350,0,40)  
pf.set_obstract(-250,0,40)  
pf.set_obstract(-150,0,40)  
pf.set_obstract(-50,0,40)  
pf.replan() 
i=0

print(pf.get_path())
len=pf.get_path().__len__()
path_x,path_y=x[0],y[0]

while True:
    ro_b_0.setSpeed(0,1,1)
while True:
    if i is len-1 or i > len-1:
        ro_b_0.setSpeed(0,0,0)
        break
    if (x[0]-pf.get_path()[i].x/100)**2+(y[0]-pf.get_path()[i].y/100)**2<0.01:
        i=i+1
        pass
    else:
        path_x=pf.get_path()[i].x/100
        path_y=pf.get_path()[i].y/100 
    
    xx,yy,success,vx,vy = P2P(ro_b_0,camera,path_x,path_y,vx,vy)
    x,y,ori=camera.getRobotPos()
    print("success=",success,"x=",x[0],"y=",y[0],"dest_x=",path_x,"dest_y=",path_y,"i=",i,"len=",len)
    if success is 1:
        i=i+1
    time.sleep(1)
ro_b_0.setSpeed(0,0,0)

