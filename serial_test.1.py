import numpy as np
from bitarray import bitarray
import struct
from SSL_Lib.Robot import *
start_package = b'\xff\xb0\x01\x02\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x31'
config_package = b'\xff\xb0\x04\x05\x06\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x85'  # 频点为0
package_1 = b'\xff\x00\x01\x01\x26\x41\x90\x28\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\x00\x00\x00'
package_2 = b'\xff\x00\x01\x01\x06\x40\x00\x28\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00'

c5 = bitarray(8)
c6 = bitarray(8)
c7 = bitarray(8)

address = ('128.0.0.1', 20011)
y2 = Robot("blue", 3,0.15,address)
a=y2.setSpeed(1,1,0)
print(a)