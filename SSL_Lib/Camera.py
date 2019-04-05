import socket
import sys

sys.path.append('SSL_Lib/')
import SSL_Lib.grSim_Packet_pb2 as grSim_Packet_pb2
import SSL_Lib.grSim_Commands_pb2 as grSim_Commands_pb2
import SSL_Lib.grSim_Replacement_pb2 as grSim_Replacement_pb2
import SSL_Lib.vision_detection_pb2 as vision_detection_pb2


class Camera:
	def __init__(self, read_addr):
		self.read_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.read_socket.bind(read_addr)
		self.vision_frame = vision_detection_pb2.Vision_DetectionFrame()

	def update_state(self):
		self.vision_data = self.read_socket.recv(4096 * 2)
		self.vision_frame = vision_detection_pb2.Vision_DetectionFrame()
		self.vision_frame.ParseFromString(self.vision_data)
		self.robot_blue = self.vision_frame.robots_blue
		self.robot_yellow = self.vision_frame.robots_yellow
		self.blue_dict = {ro.robot_id: ro for ro in self.robot_blue}
		self.yellow_dict = {ro.robot_id: ro for ro in self.robot_yellow}

	def getRobotPos(self):
		self.update_state()
		blue = sorted(self.blue_dict)  # 排序后的字典keys
		yellow = sorted(self.yellow_dict)
		x = []
		y = []
		o = []
		for ro in blue:  # 按id顺序添加进list
			x.append(self.blue_dict[ro].x )
			y.append(self.blue_dict[ro].y )
			o.append(self.blue_dict[ro].orientation)
		for ro in yellow:
			x.append(self.yellow_dict[ro].x )
			y.append(self.yellow_dict[ro].y )
			o.append(self.yellow_dict[ro].orientation)
		return x, y, o

	def getRobotVel(self):
		self.update_state()
		x = []
		y = []
		o = []
		blue = sorted(self.blue_dict)
		yellow = sorted(self.yellow_dict)
		for ro in blue:
			x.append(self.blue_dict[ro].vel_x )
			y.append(self.blue_dict[ro].vel_y )
			o.append(self.blue_dict[ro].rotate_vel)
		for ro in yellow:
			x.append(self.yellow_dict[ro].vel_x )
			y.append(self.yellow_dict[ro].vel_y )
			o.append(self.yellow_dict[ro].rotate_vel)
		return x, y, o

	def getRobotDict(self):
		self.update_state()
		for ro in self.blue_dict:  
			self.blue_dict[ro].x = self.blue_dict[ro].x / 1000
			self.blue_dict[ro].y = self.blue_dict[ro].y/ 1000
			#self.blue_dict[ro].orientation
			self.blue_dict[ro].vel_x = self.blue_dict[ro].vel_x / 1000
			self.blue_dict[ro].vel_y = self.blue_dict[ro].vel_y / 1000 
			#self.blue_dict[ro].rotate_vel
		for ro in self.yellow_dict:
			self.yellow_dict[ro].x = self.yellow_dict[ro].x / 1000
			self.yellow_dict[ro].y = self.yellow_dict[ro].y / 1000
			#self.yellow_dict[ro].orientation
			self.yellow_dict[ro].vel_x = self.yellow_dict[ro].vel_x / 1000
			self.yellow_dict[ro].vel_y = self.yellow_dict[ro].vel_y / 1000 
			#self.yellow_dict[ro].rotate_vel
		return self.blue_dict, self.yellow_dict
