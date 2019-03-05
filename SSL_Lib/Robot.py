import socket
import grSim_Packet_pb2 
import grSim_Commands_pb2
import grSim_Replacement_pb2

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
    def SetReplacement(self,x,y,dir):
        rep=self.replacement.robots.add()
        rep.x=x
        rep.y=y
        rep.dir=dir
        rep.id=self.id
        rep.yellowteam=self.isteamyellow
    def getSpeedCommand(self):
        print(self.packet)
        return self.packet.SerializeToString()
    def getRepCommand(self):
        return self.packet.SerializeToString()

if __name__ == '__main__':
    address = ('127.0.0.1',20011)  
    y2=Robot("blue",3)
    y2.SetReplacement(1,1,1)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(y2.getSpeedCommand(), address)
    s.close()    