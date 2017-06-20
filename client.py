import socket
import requests
from addict import Dict
from time import sleep

api = Dict()

api.base = 'http://pixelcanvas.io'
api.pixel = '/api/pixel'
api.online = '/api/online'

config = Dict()

config.fingerprint = "40a2ac6fa4b378a0512762058a5bec98"
config.token = 'null'
config.api = api

host = "localhost"
port = 1111

def connect(s,host,port,retry=1):
	connected = False
	try:
		print("try")
		s.connect((host, port))
		print("connected !")
		connected = True
	except ConnectionRefusedError:
		print("Connection refused")
		if retry<5:
			print("Retrying (try n°{})".format(retry+1))
			connected = connect(host,port,retry+1)
		else:
			print("Le serveur distant n'est pas joignable.")
	finally:return connected

def getPixel(host,port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connected = connect(s,host,port)
	if connected:
		s.send("getPixel".encode())
		r = s.recv(9999999)
		s.close()
		print(r.decode())
		if r.decode() != "None":
			return r.decode().split(',')
		else:
			return None
	else:
		print("Could not connect to the server.")

def placed(pixel):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connected = connect(s,host,port)
	if connected:
		data = ','.join(pixel)
		s.send(data.encode())
		r = s.recv(9999999)
		print(r.decode())
		s.close()


def placePixel(x, y, color, config=config):
	data = {
		'x': x,
		'y': y,
		'color': color,
		'fingerprint': config.fingerprint,
		'token': config.token
	}

	result = requests.post(config.api.base + config.api.pixel, json=data)
	if int(result.status_code) == 200:
		return True
	elif int(result.status_code) == 422:
		return "Token Requested"
	return False

'''	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connected = connect("localhost",1111)
	if connected:
		print("Enter command : ")
		file_name = input(">> ")
		s.send(file_name.encode())
		r = s.recv(9999999)
		s.close()
		print(r.decode(),end="\n{}\n".format("-"*15))'''

waitListEmpty = False
while not waitListEmpty:
	placed = False
	tryNB = 1

	while not placed:
		pixel = getPixel(host,port)
		if pixel==None:
			waitListEmpty, placed = True,True
			print("Dessin terminé")
		else:
			placed = placePixel(pixel[0],pixel[1],pixel[2],config)
			if placed:
				print("placed {:2} at {};{}\t\t\t\t".format(pixel[2],pixel[0],pixel[1]))
				placedPixel(pixel)
				sleep(25)
			else:
				print("could not place {:2} at {};{} (try n°{})".format(pixel[2],pixel[0],pixel[1],tryNB),end="\r")
				tryNB+=1
			sleep(5)