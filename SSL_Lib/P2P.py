import numpy as np
def P2P(x0,y0,ori0,x,y,ori):#ori给的是弧度值
    distance=((x-x0)**2+(y-y0)**2)**0.5
    if distance<2.5:
        v=0.4*x
    elif distance>5:
        v=0
    else:
        v=0.4*(5-x)
    dest_ori=np.arctan2(y-y0,x-x0)-ori0 
    if dest_ori>np.pi:#将目标点与当前方向的夹角调整为-180-180
        dest_ori=dest_ori-np.pi*2
    elif dest_ori<-np.pi:
        dest_ori=dest_ori+np.pi*2
    dest_x=distance*np.cos(dest_ori)#将路径分解为vx,vy方向
    dest_y=distance*np.sin(dest_ori)
    ori_=ori
    ori0_=ori0
    if ori<0:
        ori_=ori+np.pi*2#将方向角转换成0-360
    if ori0<0:
        ori0_=ori0+np.pi*2
    if (int)(ori_-ori0_)>0&(int)(ori_-ori0_)<np.pi:
        w=0.1#正转
    elif ori_ is ori0_:
        w=0
    else:
        w=-0.1
    vx=v*np.cos(dest_ori)
    vy=v*np.sin(dest_ori)
    return vx,vy,0

