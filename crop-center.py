import os
from PIL import Image

pathBegin = "./timelapse-300s/"
pathEnd = "./crop-center/"
alreadyCroped = []
for files in os.walk(pathEnd):
	for name in files:
		alreadyCroped.append(name)
alreadyCroped = alreadyCroped[2]

for files in os.walk(pathBegin):
	for name in files[2]:
		if name not in alreadyCroped:
			print("Cropping image {}".format(name))
			im = Image.open(pathBegin+name)
			size = im.size
			xDep = -1000 + size[0] // 2 - 42
			xEnd = +1000 + size[0] // 2 -22
			yDep = -1000 + size[1] // 2 - 42
			yEnd = +1000 + size[1] // 2 -22
			im.crop((xDep,yDep,xEnd,yEnd)).save(pathEnd+name)
		else:
			print("Skipping {}".format(name))
print("finished !")