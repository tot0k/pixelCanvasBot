import requests
from time import time, sleep
from addict import Dict


api = Dict()

api.base = 'http://pixelcanvas.io'
api.pixel = '/api/pixel'
api.online = '/api/online'

config = Dict()

config.fingerprint = "40a2ac6fa4b378a0512762058a5bec98"
config.token = 'null'
config.api = api

def place_pixel(x, y, color, config=config):
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

def load(path):
	global grid, graphGrid
	try:
		print(path)
		f = open(path,'r', encoding="utf-8")
		grid = []
		nb=0
		for lines in f:
			cells=lines.strip().split(',')
			cells = cells[:-1]
			grid+=[cells]
		f.close()
		return grid
	except:
		print("Le fichier n'existe pas.")

def generateWaitList():
	path = "7arg.txt" #input("fichier a importer ? ")
	grid = load(path)
	xDep = -58 #int(input("X depart : "))
	yDep = 2090 #int(input("Y depart : "))
	file = open("waitList.txt",'w',encoding="utf-8")
	for y in range(len(grid)):
		for x in range(len(grid[0])):
			file.write(str(xDep+int(x)) + ',' + str(yDep+int(y)) + ',' + str(grid[y][x] + '\n'))
	file.close()

def getWaitList():
	file = open("waitList.txt",'r',encoding="utf-8")
	liste = []
	for line in file:
		if line!='\n':
			liste+=[line.strip().split(',')]
	file.close()
	return liste

def modifyWaitList(liste):
	file = open("waitList.txt",'w',encoding="utf-8")
	for l in liste:
		file.write(str(l[0]) + ',' + str(l[1]) + ',' + str(l[2] + '\n'))
	file.close()

while 1:
	liste = getWaitList()
	while len(liste)!=0:
		placed = False
		tryNB = 1
		while not placed:
			placed = place_pixel(liste[0][0],liste[0][1],liste[0][2],config)
			if placed:
				print("placed {:2} at {};{}\t\t\t\t".format(liste[0][2],liste[0][0],liste[0][1]))
				liste.pop(0)
				modifyWaitList(liste)
				sleep(25)
			else:
				print("could not place {:2} at {};{} (try n°{})".format(liste[0][2],liste[0][0],liste[0][1],tryNB),end="\r")
				tryNB+=1
			sleep(5)
	generateWaitList()
