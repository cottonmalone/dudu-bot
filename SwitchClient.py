import socket
from SwitchCommands import *
from PK8 import *

HOST = 'YOUR SWITCH IP HERE'
PORT = 7331

class SwitchClient:
	def __init__(self):
		self.isConnected = False
		
	def connectToSwitch(self):
		try:

			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
			
				sock.connect((HOST, PORT))
				print("Successfully Connected to " + HOST)
				self.isConnected = True

				cmd = SwitchCommands(sock)
				pid = cmd.getGamePID()
				cmd.attachPID(pid)

				heap = cmd.getHeap()
				data, encPK8 = cmd.readMem(heap + 0x2E32206A, 0x148)

				decryptor = PK8(encPK8)
				encryptionConst = decryptor.getEncryptionConstant()
				decryptor.decrypt()
				PID = decryptor.getPID()
				IV1, IV2, IV3, IV4, IV5, IV6 = decryptor.getIVs()

				cmd.resume()
				sock.close()

				return 1, encryptionConst, PID, IV1, IV2, IV3, IV5, IV6, IV4
		except TimeoutError:
			print("Connection timed out")
			return -1, -1, -1, -1, -1, -1, -1, -1, -1
		except OSError:
			print("A fatal error has occured")
			return -1, -1, -1, -1, -1, -1, -1, -1, -1

	def getStatus(self):
		return self.isConnected
	