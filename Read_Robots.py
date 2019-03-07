import sys
sys.path.append('SSL_Lib/')
import vision_detection_pb2
import socket

ip_port = ('127.0.0.1',23334)
sk = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,0)
sk.bind(ip_port)
frame = vision_detection_pb2.Vision_DetectionFrame()
data = sk.recv(4096)
frame.ParseFromString(data)
blue=frame.robots_blue
print(blue[3])