import sys
import math
import numpy as np
sys.path.append('SSL_Lib/')
import SSL_Lib.vision_detection_pb2 as vision_detection_pb2
import SSL_Lib.grSim_Replacement_pb2 as grSim_Replacement_pb2
import SSL_Lib.grSim_Commands_pb2 as grSim_Commands_pb2
import SSL_Lib.grSim_Packet_pb2 as grSim_Packet_pb2
import socket
import struct
import time
from bitarray import bitarray

class Robot:
    control_socket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    def __init__(self, color, id, radius, control_addr):
        self.radius = radius
        self.start_package = b'\xff\xb0\x01\x02\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x31'  # 实际控制小车的起始包
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
            self.sim = False
            self.send_start_package()

    def send_start_package(self):
        self.control_socket.sendto(self.start_package, self.control_addr)

    def setSpeed(self, velnormal, veltangent, velangular,command=" "):
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
            commands=b'\xff'
            commands+=b'\x00'
            commands+=b'\x01'
            commands+=b'\x01'
            vx = int(100*veltangent)
            vy = int(100*velnormal)
            w = int(velangular*40)

            sign_vx = 0 if vx >= 0 else 1
            sign_vy = 0 if vy >= 0 else 1
            sign_w = 0 if w >= 0 else 1

            c4 = bitarray(8)
            c5 = bitarray(8)
            c6 = bitarray(8)
            c7 = bitarray(8)
            for c in [c4, c5, c6, c7]:
                c.setall(0)

            #define vx,vy,w sign
            c4[2] = sign_vx
            c5[4] = sign_vy
            c6[7] = sign_w

            

            #calc vx,vy,w bit array
            vxb = self.getVelBitarr(abs(vx))
            vyb = self.getVelBitarr(abs(vy))
            wb = self.getVelBitarr(abs(w))
            
            #change package bytes
            c4[3:8] = vxb[0:5]  # vx高5位
            c5[0:4] = vxb[5:9]  # vx低4位
            c5[5:8] = vyb[0:3]  # vy高3位
            c6[0:6] = vyb[3:9]  # vy低6位
            c6[7] = wb[0]  # w高1位
            c7[0:8] = wb[1:9]  # w低8位

            #get commands bytes
            c4_byte=self.bitarray2bytes(c4)
            c5_byte=self.bitarray2bytes(c5)
            c6_byte=self.bitarray2bytes(c6)
            c7_byte=self.bitarray2bytes(c7)
            for b in [c4_byte,c5_byte,c6_byte,c7_byte]:
                commands+=b
            for i in range(13):
                commands+=b'\x00'
            commands+=b'\x07'
            for i in range(3):
                commands+=b'\x00'
            return commands
            

    def getVelBitarr(self,v):
        #100
        v_bin_str=bin(v)
        #0b1100100
        vbs=v_bin_str.replace('0b','')
        #1100100
        vbitarr=bitarray(vbs)
        for i in range(9-len(vbitarr)):
            vbitarr.insert(0,0)
        #bitarray('00100110')
        return vbitarr
    def bitarray2bytes(self,bitarr):
        # s=bitarr.to01()
        # int_temp=int(s,2)
        # hex_temp=hex(int_temp)
        # print(hex_temp)
        hex_temp=bitarr.tobytes()
        return hex_temp
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
            

def walk(self,socket,x,y,ori):
    x0,y0,ori0=getXYA(self,socket)
    #print(x0,y0,ori0)
    if(100>x0):
        return 0,0.1,0
    if(x0-100>10):
        return 0,-0.1,0
    else:
        if(90>ori0*57.3):
            return 0,0,1
        if(ori0*57.3-90>5):
            return 0,0,-1
        else:
            if(y>y0):
                return 0,1,0
            if(y-y0>2):
                return 0,-1,0
            else:
                return 0,0,1

if __name__ == '__main__':
    address = ('128.0.0.1', 20011)
    y2 = Robot("blue", 3,0.15,address)
    y2.setSpeed(0,1,1)
