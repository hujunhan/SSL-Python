import sys
import math
import numpy as np

sys.path.append('SSL_Lib/')
import SSL_Lib.zss_debug_pb2 as zss_debug_pb2
import socket


class DBG():

	def __init__(self):
		self.debug_addr = ('127.0.0.1', 20001)
		self.debug_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.debug_pack = zss_debug_pb2.Debug_Msgs()

	def sendDebugMessage(self):
		self.debug_socket.sendto(self.debug_pack.SerializeToString(), self.debug_addr)

	def addText(self, x, y, text):
		message = self.debug_pack.msgs.add()
		message.type = 2
		message.color = 0
		text_msg = message.text
		pos = text_msg.pos
		pos.x = x
		pos.y = y
		text_msg.text = text

	def addLine(self, sx, sy, ex, ey):
		debug_msg = self.debug_pack.msgs.add()
		debug_msg.type = zss_debug_pb2.Debug_Msg.LINE
		debug_msg.color = zss_debug_pb2.Debug_Msg.GREEN
		debug_msg.line.start.x = sx
		debug_msg.line.start.y = -sy
		debug_msg.line.end.x = ex
		debug_msg.line.end.y = -ey
		debug_msg.line.FORWARD = False
		debug_msg.line.BACK = False

	def addPath(self, path):
		for i in range(len(path) - 1):
			self.addLine(path[i].x * 10, path[i].y * 10, path[i + 1].x * 10, path[i + 1].y * 10)
