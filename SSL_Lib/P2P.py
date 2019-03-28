import numpy as np
from SSL_Lib.Robot import *
def P2P(robot,camera,dest_x,dest_y):
    x, y, ori = camera.getRobotPos()
    vx,vy,w=0,0,0
    distance0=((x[0]-dest_x)**2+(y[0]-dest_y)**2)**0.5
    ay=(dest_x-x[0])/distance0/50
    ax=(dest_y-y[0])/distance0/50
    while True:
       #print(getXY("blue",0,read_socket))
        x, y, ori = camera.getRobotPos()
        distance=((x[0]-dest_x)**2+(y[0]-dest_y)**2)**0.5
        if distance>distance0+0.5:
            robot.setSpeed(0,0,0)
            return x,y,-1
        if(distance>0.5*distance0):
            if abs(vx)<2 and abs(vy)<2:
                vx=vx+ax
                vy=vy+ay
       # else:
       #     if abs(vx)>ax and abs(vy)>ay:
       #         vx=vx-ax
       #         vy=vy-ay
       #     else:
       #         vx,vy=0,0
       #         robot.setSpeed(vx,vy,w)
       #         x, y, ori = camera.getRobotPos()
       #         return x,y,0#0表示未到达目的地，1表示成功到达
        robot.setSpeed(vx,vy,w)
        #print("vx=",vx,"vy=",vy,"w=",w)
        #print("x=",x[0],"y=",y[0],"distance=",distance)
        if distance<0.1:
            #print("Success!")
            robot.setSpeed(0,0,0)
            return x,y,1