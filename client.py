import socket
import requests
from addict import Dict
from time import sleep

'''
TODO: 
HUD
verify fingerprint (erreur de placement)
alert try +10 (have to do the captcha)
client disconection when connected --> server crash
'''
api = Dict()

api.base = 'http://pixelcanvas.io'
api.pixel = '/api/pixel'
api.online = '/api/online'
api.bigchunk = '/api/bigchunk'

config = Dict()

config.fingerprint = "40a2ac6fa4b378a0512762058a5bec98" # Your Fingerprint
config.token = 'null'
config.api = api

host = "2.9.55.24" # Your server's IP
port = 1111
token = "user"

def connect(s,host,port,retry=1):
	connected = False
	try:
		s.connect((host, port))
		print("[INFO] Connected to the server.")
		connected = True
	except ConnectionRefusedError:
		if retry<5:
			print("[INFO] Trying to reach server (try n°{})".format(retry+1))
			connected = connect(s,host,port,retry+1)
	finally:return connected

def getPixel(host,port,token):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connected = connect(s,host,port)
	if connected:
		s.send("getPixel token:{}".format(token).encode())
		r = s.recv(9999999)
		s.close()
		if r.decode() != "None" and r.decode().split(' ')[0] != "[ERROR]":
			print("[INFO] trying to place pixel {}".format(r.decode()))
			return r.decode().split(',')
		else:return None
	else:
		print("[ERROR] Could not connect to the server.")

def placedPixel(pixel,token):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connected = connect(s,host,port)
	if connected:
		data = "placed token:{},x:{},y:{},color:{}".format(token,pixel[0],pixel[1],pixel[2])
		s.send(data.encode())
		r = s.recv(65536)
		print(r.decode())
		s.close()

def generate(path,x,y,token):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connected = connect(s,host,port)
	if connected:
		data = "generate token:{},x:{},y:{},path:{}".format(token,x,y,path)
		s.send(data.encode())
		r = s.recv(65536)
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

#generate("reno.txt",214,2492,token)

waitListEmpty = False
while not waitListEmpty:
	placed = False
	tryNB = 1
	pixel = getPixel(host,port,token)

	while not placed:
		if pixel==None:
			waitListEmpty, placed = True,True
		else:
			placed = placePixel(pixel[0],pixel[1],pixel[2],config)
			if placed:
				print("[INFO] Placed {} at {};{}\t\t\t\t".format(pixel[2],pixel[0],pixel[1]))
				placedPixel(pixel,token)
				sleep(25)
			else:
				print("[ERROR] Could not place {} at {};{} (try n°{})".format(pixel[2],pixel[0],pixel[1],tryNB))
				tryNB+=1
			sleep(5)