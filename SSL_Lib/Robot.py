import sys
sys.path.append('SSL_Lib/')
import SSL_Lib.vision_detection_pb2 as vision_detection_pb2
import SSL_Lib.grSim_Replacement_pb2 as grSim_Replacement_pb2
import SSL_Lib.grSim_Commands_pb2 as grSim_Commands_pb2
import SSL_Lib.grSim_Packet_pb2 as grSim_Packet_pb2
import socket
import struct
import time


class Robot:
    control_socket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    def __init__(self, color, id, radius, control_addr):
        self.radius = radius
        self.start_package = b'\xF0\x5A\x5A\x01\x01\xA6'  # 实际控制小车的起始包
        self.control_addr = control_addr  # 控制的地址
        self.control_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.packet = grSim_Packet_pb2.grSim_Packet()  # packet类，由commands和replacements组成
        self.commands = self.packet.commands
        self.replacement = self.packet.replacement
        self.id = id
        if(color is "yellow"):
            self.isteamyellow = True
        else:
            self.isteamyellow = False
        if self.control_addr[0] is not '127.0.0.1':
            self.sim = True
            self.send_start_package()

    def send_start_package(self):
        self.control_socket.sendto(self.start_package, self.control_addr)

    def setSpeed(self, velnormal, veltangent, velangular):
        if self.sim is True:
            self.commands.timestamp = 0
            self.commands.isteamyellow = self.isteamyellow
            rc = self.commands.robot_commands.add()
            rc.id = self.id
            rc.kickspeedx = 0
            rc.kickspeedz = 0
            rc.velnormal = velnormal  # 设置垂直速度
            rc.velangular = velangular  # 设置角速度
            rc.veltangent = veltangent  # 设置箭头方向速度
            rc.spinner = False
            rc.wheelsspeed = False
            self.sendCommand()  # 发送指令
        else:
            robot_num=0
            vx = int(100*veltangent)
            vy = int(100*velnormal)
            w = int(velangular*40)
            send_package = [b'\x00' for i in range(25)]
            send_package[0] = b'\x48'
            send_package[1] = struct.pack('!B', robot_num)
            sign_vx = 0 if vx >= 0 else 1
            sign_vy = 0 if vy >= 0 else 1
            sign_w = 0 if w >= 0 else 1
            send_package[2] = struct.pack('!B', sign_vx*128 + abs(vx) % 128)
            send_package[3] = struct.pack('!B', sign_vy*128 + abs(vy) % 128)
            send_package[4] = struct.pack('!B', sign_w * 128 + abs(w) % 128)
            send_package[17] = struct.pack(
                '!B', int(abs(w)/128) + int(abs(vy)/128)*16 + int(abs(vx)/128)*64)
            package = struct.pack('!25c', send_package[0], send_package[1], send_package[2], send_package[3], send_package[4], send_package[5], send_package[6], send_package[7], send_package[8], send_package[9], send_package[10], send_package[11],
                                  send_package[12], send_package[13], send_package[14], send_package[15], send_package[16], send_package[17], send_package[18], send_package[19], send_package[20], send_package[21], send_package[22], send_package[23], send_package[24])
            self.control_socket.sendto(package,self.control_addr)
    def setReplacement(self, x, y, dir):
        rep = self.replacement.robots.add()
        rep.x = x  # 设置位置
        rep.y = y  # 设置位置
        rep.dir = dir  # 设置方向
        rep.id = self.id  # 设置id
        rep.yellowteam = self.isteamyellow
        self.sendCommand()  # 发送指令

    def clearCommand(self):
        self.packet.Clear()
        self.commands = self.packet.commands
        self.replacement = self.packet.replacement

    def getSpeedCommand(self, debug=False):
        if debug is True:
            print(self.packet)
        return self.packet.SerializeToString()


    def sendCommand(self):
        try:
            Robot.control_socket.sendto(
                self.getSpeedCommand(), self.control_addr)
        except OSError as e:
            Robot.control_socket=Robot.control_socket.dup()
            print('oserror!')
            


if __name__ == '__main__':
    address = ('127.0.0.1', 20011)
    y2 = Robot("blue", 3)
    y2.SetReplacement(1, 1, 1)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(y2.getSpeedCommand(), address)
    s.close()
