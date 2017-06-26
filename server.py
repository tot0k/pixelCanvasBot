#!/usr/bin/env python
# coding: utf-8 

import socket
import threading
import time
from random import randint

class ClientThread(threading.Thread):
	'''Class called when a client connects to the server'''

	def __init__(self, ip, port, clientsocket):
		threading.Thread.__init__(self)
		self.ip = ip
		self.port = port
		self.clientsocket = clientsocket
		print("[+] New thread for {}:{}".format(self.ip, self.port, ))

	def run(self): 
		global tokens, admins
		print("Connection de %s %s" % (self.ip, self.port, ))

		r = self.clientsocket.recv(2048)	# Waiting for request from client
		rUtf8 = r.decode()	# Translating Bytes to utf-8

		command = rUtf8.split(" ")[0]
		data = dict((k.strip(), v.strip()) for k,v in (item.split(':') for item in rUtf8.split(" ")[1].split(',')))

		if data['token'] in tokens or data['token'] in admins:
			print("token {} accepted".format(data['token']))
			if command == "getPixel":
				self.getPixel()

			elif command == "placed":
				self.pixelPlaced(data)

			elif command == "generate":
				if data['token'] in admins:
					generated = generatewaitList(data)
					if generated:
						self.clientsocket.send("[INFO] Successfuly generated the waitlist from {}".format(data['path']).encode())
					else:
						self.clientsocket.send("[ERROR]".encode())
				else:
					self.clientsocket.send("[ERROR] Bad token : {}".format(data['token']).encode())

			else:
				self.clientsocket.send("[ERROR] Incorrect command {}".format(data).encode())
		else:
			self.clientsocket.send("[ERROR] Bad token : {}".format(data['token']).encode())

		print("[-] Client {}:{} disconnected.".format(self.ip,self.port),end="\n{}\n".format("-"*15))

	def getPixel(self):
		global waitList
		if len(waitList)>0:
			data = waitList[randint(0,len(waitList)-1)]
			print("getPixel > {}".format(",".join(data)))
			self.clientsocket.send(",".join(data).encode())
		else:
			self.clientsocket.send("None".encode())

	def pixelPlaced(self,data):
		pixel = [data['x'],data['y'],data['color']]
		print("Pixel placed > {}".format(pixel))
		try:
			waitList.pop(waitList.index(pixel))
			print("pixel deleted from waitList")
		except:
			print("pixel does not exist")
		self.clientsocket.send("[INFO] Pixel removed from waitlist".encode())


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
	grid = load(data['path'])
	if grid != None:
		xDep = int(data['x'])
		yDep = int(data['y'])

		file = open("waitList.txt",'w',encoding="utf-8")
		for y in range(len(grid)):
			for x in range(len(grid[0])):
				file.write(str(xDep+x) + ',' + str(yDep+y) + ',' + str(grid[y][x] + '\n'))
		file.close()
		waitList = getWaitList()
		print("waitList generated from {}".format(data['path']))
		return True
	else:
		print("File not found : {}".format(data['path']))
		return False


def getTokens():
	tokens, admins = [], []
	
	try:
		file = open("tokens",'r',encoding="utf-8")
		for line in file:
			tokens+=[line.strip()]
		file.close()
	except FileNotFoundError:
		print("ERROR : tokens file not found")

	try:
		file = open("admins",'r',encoding="utf-8")
		for line in file:
			admins+=[line.strip()]
		file.close()
	except FileNotFoundError:
		print("ERROR : admins file not found")

	return tokens,admins

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("",1111))

waitList = getWaitList()
tokens,admins = getTokens()

waitThread = WaitThread()
waitThread.start()

while True:
	s.listen(10)
	print( "Listening...")
	(clientsocket, (ip, port)) = s.accept()
	newthread = ClientThread(ip, port, clientsocket)
	newthread.start()