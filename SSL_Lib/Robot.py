import socket
import sys
sys.path.append('SSL_Lib/')
import SSL_Lib.grSim_Packet_pb2 as grSim_Packet_pb2
import SSL_Lib.grSim_Commands_pb2 as grSim_Commands_pb2
import SSL_Lib.grSim_Replacement_pb2 as grSim_Replacement_pb2
import SSL_Lib.vision_detection_pb2 as vision_detection_pb2
class Robot:
    def __init__(self, color,id,radius,control_addr):
        self.radius=radius
        self.control_addr=control_addr #控制的地址
        self.control_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.packet=grSim_Packet_pb2.grSim_Packet() #packet类，由commands和replacements组成
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
        rc.velnormal=velnormal #设置垂直速度
        rc.velangular=velangular #设置角速度
        rc.veltangent=veltangent #设置箭头方向速度
        rc.spinner=False
        rc.wheelsspeed=False
        self.sendCommand() #发送指令
    def setReplacement(self,x,y,dir):
        rep=self.replacement.robots.add()
        rep.x=x #设置位置
        rep.y=y #设置位置
        rep.dir=dir #设置方向
        rep.id=self.id #设置id
        rep.yellowteam=self.isteamyellow
        self.sendCommand() #发送指令
    def clearCommand(self):
        self.packet.Clear()
        self.commands=self.packet.commands
        self.replacement=self.packet.replacement
    def getSpeedCommand(self,debug=False):
        if debug is True:
            print(self.packet)
        return self.packet.SerializeToString()
    def sendCommand(self):
        self.control_socket.sendto(self.getSpeedCommand(),self.control_addr)

if __name__ == '__main__':
    address = ('127.0.0.1',20011)  
    y2=Robot("blue",3)
    y2.SetReplacement(1,1,1)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(y2.getSpeedCommand(), address)
    s.close()