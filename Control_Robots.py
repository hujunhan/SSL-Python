import sys
sys.path.append('SSL_Lib/')
import socket
from Robot import *

address = ('127.0.0.1',20011)  
y2=Robot("blue",5)
y2.SetReplacement(1,1,1)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
    s.sendto(y2.getSpeedCommand(), address)
s.close()
