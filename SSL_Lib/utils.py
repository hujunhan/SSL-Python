import numpy as np
def calc_angle(start,goal):
    #起始点的信息
    start_x=start.x
    start_y=start.y
    start_ori=start.orientation

    #终点的信息
    goal_x=goal.x
    goal_y=goal.y

    #起点指向终点的角度
    vector_angle=np.arctan2(goal_y-start_y,goal_x-start_x)
    #print(vector_angle)
    #要返回的angle，但是范围有可能超出-pi-pi
    angle=start_ori-vector_angle
    if(angle>np.pi):
        angle=angle-np.pi*2
    if(angle<-np.pi):
        angle=angle+np.pi*2
    return angle

def calc_distance(start,goal):
    return np.hypot(goal.y-start.y,goal.x-start.x)
