#!/usr/bin/env python
# coding: utf-8 

import socket
import threading
import time
from random import randint

class ClientThread(threading.Thread):

	def __init__(self, ip, port, clientsocket):

		threading.Thread.__init__(self)
		self.ip = ip
		self.port = port
		self.clientsocket = clientsocket
		print("[+] Nouveau thread pour %s %s" % (self.ip, self.port, ))

	def run(self): 
   
		print("Connection de %s %s" % (self.ip, self.port, ))

		r = self.clientsocket.recv(2048)
		data = r.decode()

		if data.split(' ')[0] == "getPixel":
			self.getPixel(" ".join(data.split(" ")[1:]))
		elif data.split(' ')[0] == "placed":
			self.pixelPlaced(" ".join(r.decode().split(" ")[1:]))
		elif data.split(' ')[0] == "generate":
			generated = generatewaitList(" ".join(r.decode().split(" ")[1:]))
			if generated:
				self.clientsocket.send("OK".encode())
			else:
				self.clientsocket.send("ERROR".encode())
		else:
			self.clientsocket.send("Instruction incorrecte : {}".format(data).encode())

		print("Client déconecté...",end="\n{}\n".format("-"*15))

	def getPixel(self,data):
		global waitList
		print("getPixel")
		if len(waitList)>0:
			data = waitList[randint(0,len(waitList)-1)]
			self.clientsocket.send(",".join(data).encode())
		else:
			self.clientsocket.send("None".encode())

	def pixelPlaced(self,data):
		print("Pixel placed")
		data = data.split(',')
		try:
			waitList.pop(waitList.index(data))
			print("pixel deleted from waitList")
		except:
			print("pixel does not exist")
		self.clientsocket.send("OK".encode())


class WaitThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.startTime = time.time()
		self.stop = False

	def run(self): 
		while not self.stop:
			if time.time()-self.startTime >= 60:
				print("Saving waitList...")
				saveWaitlist()
				self.startTime = time.time()


def getWaitList():
	try:
		file = open("waitList.txt",'r',encoding="utf-8")
		liste = []
		for line in file:
			if line!='\n':
				liste+=[line.strip().split(',')]
		file.close()
		return liste
	except FileNotFoundError:
		print("Le fichier n'existe pas et a été créé")
		file = open("waitList.txt",'w',encoding="utf-8")
		file.close()

def saveWaitlist():
	file = open("waitList.txt",'w',encoding="utf-8")
	for l in waitList:
		file.write(str(l[0]) + ',' + str(l[1]) + ',' + str(l[2] + '\n'))
	file.close()
	print("WaitList saved.")

def load(path):
	try:
		path = "img/" + path
		file = open(path,'r', encoding="utf-8")
		grid = []
		nb=0
		for lines in file:
			cells=lines.strip().split(',')
			cells = cells[:-1]
			grid+=[cells]
		file.close()
		return grid
	except:return None

def generatewaitList(data):
	global waitList
	data = data.split(',')
	if data[3] == "totok": # Verif token
		grid = load(data[0])
		if grid != None:
			xDep = int(data[1])
			yDep = int(data[2])

			file = open("waitList.txt",'w',encoding="utf-8")
			for y in range(len(grid)):
				for x in range(len(grid[0])):
					file.write(str(xDep+x) + ',' + str(yDep+y) + ',' + str(grid[y][x] + '\n'))
			file.close()
			waitList = getWaitList()
			print("waitList generated from {}".format(data[0]))
			return True
		else:
			print("File not found : {}".format(data[0]))
			return False
	else:
		print("Bad Token")
		return False

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("",1111))

waitList = getWaitList()

waitThread = WaitThread()
waitThread.start()

while True:
	s.listen(10)
	print( "En écoute...")
	(clientsocket, (ip, port)) = s.accept()
	newthread = ClientThread(ip, port, clientsocket)
	newthread.start()