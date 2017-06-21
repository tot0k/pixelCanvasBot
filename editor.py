from tkinter import *
from time import time
import os

WIDTH = 1920
HEIGHT = 1000

states = ["white",'light grey',"grey",'black','pink',"red",'gold','brown',"yellow","Lime","green","cyan","RoyalBlue1","blue","DarkOrchid1","purple"]
selectedColor = 1
clickDown = False
borderValue = 1

# Détermine les positions en x et y de la case cliquée
def position(event):
	itemId = main.find_overlapping(event.x-1,event.y-1,event.x+1,event.y+1)[0]
	for i in range(len(graphGrid)):
		x=-1
		if itemId in graphGrid[i]:
			x = graphGrid[i].index(itemId)
			return x,i

# Change la valeur de la case cliquée suivant la valeur active "selectedColor"
def leftClickEditor(event):
	global grid, states
	x,y = position(event)
	if grid[y][x]!=selectedColor:
		grid[y][x] = selectedColor
		changeState(x,y,selectedColor)

def rightClick(event):
	global grid, states
	x,y = position(event)
	grid[y][x] = 0
	changeState(x,y,0)

def leftClickDown(event):
	global clickDown
	clickDown = True
	leftClickEditor(event)

def leftClickUp(event):
	global clickDown
	clickDown = False
	return

def motion(event):
	global clickDown
	if clickDown:
		try:
			leftClickEditor(event)
		except:pass


# Entoure en noir le rectangle de couleur selectionné
def changeTileType(event):
	global tileChange, sideBar, selectedColor
	try :
		itemId = sideBar.find_overlapping(event.x-1,event.y-1,event.x+1,event.y+1)[0]
		if itemId in sideBar.find_withtag("palette"):
			for i in tileChange:
				sideBar.itemconfigure(i,width=0)
			sideBar.itemconfigure(itemId,width=2)
			selectedColor = tileChange.index(itemId)
	except:pass


# Enregistre un labyrinthe dans un fichier
def save(path):
	global grid
	path = "img/" + path
	os.makedirs(os.path.dirname(path), exist_ok=True)
	file = open(path,'w',encoding="utf-8")
	for y in grid:
		for x in y:
			file.write(str(x)+',')
		file.write('\n')
	file.close()
	print("saved")


# Charge un labyrinthe à partir d'un fichier
def load(path):
	global grid, graphGrid
	try:
		path = "img/" + path
		print(path)
		f = open(path,'r', encoding="utf-8")
		grid = []
		nb=0
		for lines in f:
			cells=lines.strip().split(',')
			cells = cells[:-1]
			grid+=[cells]
		f.close()

		main.delete(ALL)

		graphGrid = [[0 for j in range(len(grid[0]))] for i in range(len(grid))]
		drawGrid(len(grid[0]),len(grid))
		main.update()
	except:
		print("Le fichier n'existe pas.")


# Crée un nouveau labyrinthe de taille x,y (ou de taille par défaut 20,20)
def new(strX,strY):
	global grid, graphGrid
	print(strX,strY)
	try:
		if strX=="x" and strY=="y":
			x,y=20,20
		else:		
			x = int(strX)
			y = int(strY)
		grid, graphGrid = [[0 for j in range(x)] for i in range(y)],[[0 for j in range(x)] for i in range(y)]
		main.delete(ALL)
		drawGrid(x,y)
		main.update()
	except:
		print("Valeurs incorrectes.")



def bordures():
	global borderValue, graphGrid, changeBorder
	if borderValue==0:
		borderValue=1
	else:
		borderValue=0

	main.delete(ALL)
	drawGrid(len(graphGrid[0]),len(graphGrid))



def initInterface():
	global fen, main, WIDTH, HEIGHT, states, tileChange, sideBar, changeBorder
	# Création de la fenêtre
	fen = Tk()
	fen.title("Maze Editor")
	main = Canvas(fen, width=WIDTH, height=HEIGHT, bg="grey86",border=0)
	sideBar = Canvas(fen, width=200, height=HEIGHT, bg="grey86",border=0)
	fen.resizable(0,0)

	# Nom du labyrinthe
	fileName = StringVar()
	fileName.set("default")
	name = Entry(sideBar, textvariable=fileName, width=27)

	# Taille du labyrinthe à créer
	xLenght	= StringVar()
	yLenght	= StringVar()
	xLenght.set("x")
	yLenght.set("y")

	xEntry	= Entry(sideBar, textvariable=xLenght, width=10)
	yEntry	= Entry(sideBar, textvariable=yLenght, width=10)


	# BUTTONS
	saveButton	= Button(sideBar, text = "Enregistrer", command = lambda : save(fileName.get()+".txt"), width=10)
	loadButton	= Button(sideBar, text = "Charger", command = lambda : load(fileName.get()+".txt"), width=10)
	newButton	= Button(sideBar, text = "Nouveau", command = lambda : new(xLenght.get(),yLenght.get()))
	changeBorder= Button(sideBar, text = "Cacher/Afficher Bordures", command = bordures)

	# Placing elements
	name.place(x=20,y=20)
	saveButton.place(x=20,y=50)
	loadButton.place(x=110,y=50)

	xEntry.place(x=20,y=90)
	yEntry.place(x=100,y=90)
	newButton.place(x=20,y=120,width=64)

	sideBar.create_line(0,155,200,155,fill="grey")
	
	# Colors
	tileChange = [sideBar.create_rectangle(20,170+25*i+i*10,150,170+25*(i+1)+i*10, fill=states[i], width=0, tag="palette") for i in range(len(states))]
	sideBar.itemconfigure(tileChange[states.index("white")],width="2")

	changeBorder.place(x=25,y=730,width=150)

	sideBar.pack(side = LEFT)
	main.pack(side = LEFT)

	main.bind("<Button-1>", leftClickDown)
	main.bind("<Button-3>", rightClick)
	main.bind("<ButtonRelease-1>", leftClickUp)
	main.bind("<Motion>", motion)

	sideBar.bind("<Button-1>", changeTileType)


def drawGrid(lenX,lenY):
	global WIDTH, HEIGHT, states, grid, graphGrid, borderValue

	cellX = (WIDTH-200)//lenX
	cellY = HEIGHT//lenY

	if cellX > cellY:
		cellWidth=cellY
	else:
		cellWidth=cellX

	if cellWidth*lenY < 800:
		ySize = 800
	else:
		ySize = cellWidth*lenY

	print("Cellules de {}px\n {}x{}".format(cellWidth,cellWidth*lenX, ySize))
	fen.geometry("{}x{}".format(lenX*cellWidth+205,ySize))

	for y in range(lenY):
		for x in range(lenX):
			graphGrid[y][x] = main.create_rectangle(x*cellWidth,y*cellWidth,(x+1)*cellWidth,(y+1)*cellWidth,outline="light grey", width=borderValue, fill = states[int(grid[y][x])])

	return grid, graphGrid

def changeState(x,y,state):
	global states, main
	main.itemconfigure(graphGrid[y][x],fill=states[state])

if __name__ == '__main__':
	global grid, graphGrid
	grid, graphGrid = [[0 for j in range(20)] for i in range(20)],[[0 for j in range(20)] for i in range(20)]
	initInterface()
	load("img/default.txt")
	fen.mainloop()
