import serial

#打开串口
serialPort="COM3"   #串口
baudRate=100000       #波特率
ser=serial.Serial(serialPort,baudRate,timeout=0.5)  
print(ser.isOpen())
print ("参数设置：串口=%s ，波特率=%d"%(serialPort,baudRate))
#start_package = b'\xff\xb0\x01\x02\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x31'
#//package_1=      b'\xff\x00\x01\x01\x26\x41\x90\x28\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00'
#收发数据
#//ser.write(start_package)
while True:
    a=ser.readline()
    if a is not b'':
        print(ser.readline())#可以接收中文
#//ser.write(package_1)
#//print(ser.readline())#可以接收中文
ser.close()  
