import socket
import sys
sys.path.append('SSL_Lib/')
import SSL_Lib.grSim_Packet_pb2 as grSim_Packet_pb2
import SSL_Lib.grSim_Commands_pb2 as grSim_Commands_pb2
import SSL_Lib.grSim_Replacement_pb2 as grSim_Replacement_pb2
import SSL_Lib.vision_detection_pb2 as vision_detection_pb2

class Camera:
    def __init__(self,read_addr):
        self.read_socket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.read_socket.bind(read_addr)
        self.vision_frame = vision_detection_pb2.Vision_DetectionFrame()
    def update_state(self):
        self.vision_data=self.read_socket.recv(4096)
        self.vision_frame=vision_detection_pb2.Vision_DetectionFrame()
        self.vision_frame.ParseFromString(self.vision_data)
        self.robot_blue=self.vision_frame.robots_blue
        self.robot_yellow=self.vision_frame.robots_yellow
        
    
    def getRobotPos(self):
        self.update_state()
        x=[]
        y=[]
        o=[]
        for ro in self.robot_blue:
            x.append(ro.x/1000)
            y.append(ro.y/1000)
            o.append(ro.orientation)
        for ro in self.robot_yellow:
            x.append(ro.x/1000)
            y.append(ro.y/1000)
            o.append(ro.orientation)
        return x,y,o

        