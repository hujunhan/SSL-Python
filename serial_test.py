import serial
from bitarray import bitarray
import struct
from SSL_Lib.Robot import *
#打开串口
serialPort="COM3"   #串口
baudRate=115200      #波特率
ser=serial.Serial(serialPort,baudRate,timeout=0.5)  
print(ser.isOpen())
print ("参数设置：串口=%s ，波特率=%d"%(serialPort,baudRate))
start_package = b'\xff\xb0\x01\x02\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x31'
config_package= b'\xff\xb0\x04\x05\x06\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x85'#频点为0
package_1=      b'\xff\x00\x01\x01\x26\x41\x90\x28\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\x00\x00\x00'
package_2=      b'\xff\x00\x01\x01\x06\x40\x00\x28\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\x00\x00\x00'
#收发数据
address = ('128.0.0.1', 20011)
y2 = Robot("blue", 3,0.15,'COM5')
a=y2.setSpeed(0,0.1,0)
pac_test=a
while True:
    a=ser.write(start_package)
    a=ser.readline()
    if a is not b'':
        print(a)
        #a might be b'\xff\xb0"\xcfV\xd6\x10qE\x98\x00!\x82V\xa9\x11\x00\x00\x00\x00\x00\x00\x00\x00n'
        break
a=ser.write(config_package)
import time
#time.sleep(5)
while True:
    a=ser.write(pac_test)
    a=ser.readline()
    if a is not b'':
        print(a)
        break
