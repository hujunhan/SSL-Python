import socket
import sys
import math
import numpy as np
sys.path.append('SSL_Lib/')
import SSL_Lib.grSim_Packet_pb2 as grSim_Packet_pb2
import SSL_Lib.grSim_Commands_pb2 as grSim_Commands_pb2
import SSL_Lib.grSim_Replacement_pb2 as grSim_Replacement_pb2
import SSL_Lib.vision_detection_pb2 as vision_detection_pb2
class Robot:
    def __init__(self, color,id):
        self.packet=grSim_Packet_pb2.grSim_Packet()
        self.commands=self.packet.commands
        self.replacement=self.packet.replacement
        self.id=id
        if(color is "yellow"):
            self.isteamyellow=True 
        else:
            self.isteamyellow=False
    def setSpeed(self,velnormal,veltangent,velangular):
        self.commands.timestamp=0
        self.commands.isteamyellow=self.isteamyellow
        rc=self.commands.robot_commands.add()
        rc.id=self.id
        rc.kickspeedx=0
        rc.kickspeedz=0
        rc.velnormal=velnormal
        rc.velangular=velangular
        rc.veltangent=veltangent
        rc.spinner=False
        rc.wheelsspeed=False
    def setReplacement(self,x,y,dir):
        rep=self.replacement.robots.add()
        rep.x=x
        rep.y=y
        rep.dir=dir
        rep.id=self.id
        rep.yellowteam=self.isteamyellow
    def clearCommand(self):
        self.packet.Clear()
        self.commands=self.packet.commands
        self.replacement=self.packet.replacement
    def getSpeedCommand(self,debug=False):
        if debug is True:
            print(self.packet)
        return self.packet.SerializeToString()


def getPos(self,socket):
    id=self.id
    if(self.isteamyellow is True):
        color="yellow" 
    else:
        color="blue"
    vision_data=socket.recv(4096)
    vision_frame=vision_detection_pb2.Vision_DetectionFrame()
    vision_frame.ParseFromString(vision_data)
    robot_blue=vision_frame.robots_blue
    robot_yellow=vision_frame.robots_yellow
    #print(len(robot_blue),len(robot_yellow))
    if(color is "blue"):
        return robot_blue[id]
    else:
        return robot_yellow[id]

def getXYA(self,socket):
    id=self.id
    if(self.isteamyellow is True):
        color="yellow" 
    else:
        color="blue"
    vision_data=socket.recv(4096)
    vision_frame=vision_detection_pb2.Vision_DetectionFrame()
    vision_frame.ParseFromString(vision_data)
    robot_blue=vision_frame.robots_blue
    robot_yellow=vision_frame.robots_yellow
    #print(len(robot_blue),len(robot_yellow))
    if(color is "blue"):
        return robot_blue[id].x,robot_blue[id].y,robot_blue[id].orientation
    else:
        return robot_yellow[id].x,robot_yellow[id].y,robot_yellow[id].orientation

def walk(self,socket,x,y,ori):
    x0,y0,ori0=getXYA(self,socket)
    dis=np.sqrt(np.square(x-x0)+np.square(y-y0))
    if((ori-ori0)*57.3>1):
        w=0
    else:
        w=1
    return 0,1,w

if __name__ == '__main__':
    address = ('127.0.0.1',20011)  
    y2=Robot("blue",3)
    y2.SetReplacement(1,1,1)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(y2.getSpeedCommand(), address)
    s.close()