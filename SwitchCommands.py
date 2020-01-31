import socket
import struct
import time
from PK8 import *

COMMAND_STATUS = 0x01
COMMAND_POKE8 = 0x02
COMMAND_POKE16 = 0x03
COMMAND_POKE32 = 0x04
COMMAND_POKE64 = 0x05
COMMAND_READ = 0x06
COMMAND_WRITE = 0x07
COMMAND_CONTINUE = 0x08
COMMAND_PAUSE = 0x09
COMMAND_ATTACH = 0x0A
COMMAND_DETACH = 0x0B
COMMAND_QUERY_MEMORY = 0x0C
COMMAND_QUERY_MEMORY_MULTI = 0x0D
COMMAND_CURRENT_PID = 0x0E
COMMAND_GET_ATTACHED_PID = 0x0F
COMMAND_GET_PIDS = 0x10
COMMAND_GET_TITLEID = 0x11
COMMAND_DISCONNECT = 0x12
COMMAND_READ_MULTI = 0x13
COMMAND_SET_BREAKPOINT = 0x14

class SwitchCommands:

	def __init__(self, socket):
		self.socket = socket

	def getPIDs(self, length):
		rawPIDList = self.socket.recv(1024)

		pidList = list()

		i = 0
		while i < length:
			pidList.append(rawPIDList[i * 8])
			i += 1

		return pidList

	def bytesToInt(self, bytedata, length):
		#print("\nbytes: " + bytedata.hex())
		i = 0
		j = 0
		data = list()
		arr = list()
		dispData = list()
		while i < (length/4):
			arr.append(hex(struct.unpack("I", bytedata[j + 13 : j + 17])[0]))
			j += 4
			i += 1

		j = 0
		while j < length:
			dispData.append(hex(bytedata[j+13]))
			data.append(bytedata[j+13])
			j += 1

		#print("data: " + str(dispData))
		#print("length: " + str(len(dispData)))
		#print(str(arr))
		return arr, data

	def getGamePID(self):
		self.socket.send(bytes({COMMAND_GET_PIDS}))
		count = self.socket.recv(1024)
		length = int(count[0])

		dataList = self.getPIDs(length)
		return int(dataList[length - 1])

	def resume(self):
		self.socket.send(bytes({COMMAND_CONTINUE}))

	def getCurrentPid(self):
		self.socket.send(bytes({COMMAND_CURRENT_PID}))
		return self.socket.recv(1024)[0]

	def pause(self):
		self.socket.send(bytes({COMMAND_PAUSE}))

	def detachPID(self):
		self.socket.send(bytes({COMMAND_DETACH}))

	def readMem(self, addr, size):
		data = [COMMAND_READ]
		data[1:9] = struct.pack("Q", addr)
		data[9:13] = struct.pack("I", size)

		while True:
			self.socket.send(bytes(data))
			rawReadReply = self.socket.recv(2048)
			#print("\nbytes: " + rawReadReply.hex())

			while len(rawReadReply) < 16:
				self.socket.send(bytes(data))
				rawReadReply = self.socket.recv(2048)

			length = int(struct.unpack("I", rawReadReply[9:13])[0])
			check = int(struct.unpack("I", rawReadReply[0:4])[0])
			if length == size and check == 0:
				return self.bytesToInt(rawReadReply, length)

	def getHeap(self):
		data = [COMMAND_QUERY_MEMORY_MULTI]
		data[1:9] = struct.pack("Q", 0)
		data[9:13] = struct.pack("I", 10000)
		self.socket.send(bytes(data))
		time.sleep(1.0)
		
		rawMemReg = bytes(self.socket.recv(280008)) # 10000 * 28 + 8
		rawMemRegLen = len(rawMemReg)

		while len(rawMemReg) < 16:
			rawMemReg = bytes(self.socket.recv(280008)) # 10000 * 28 + 8
			rawMemRegLen = len(rawMemReg)

		i = 4 # ignore 1st 4 0 bytes
		while i < rawMemRegLen - 4	: # ignore last 4 0 bytes
			v = struct.unpack("Q", rawMemReg[i : i + 8])[0]
			if struct.unpack("I", rawMemReg[i + 16 : i + 20])[0] == 5 :
				return struct.unpack("Q", rawMemReg[i : i + 8])[0]
			i += 0x1C

		print("Heap not found")
		time.sleep(0.1)

	def attachPID(self, pid):
		data = [COMMAND_ATTACH]
		data[1:9] = struct.pack("Q", pid)
		self.socket.send(bytes(data))
		time.sleep(0.1)


	


