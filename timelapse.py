#!/usr/bin/env python3

import requests
from PIL import Image
from time import strftime, sleep, time

colors = [(255, 255, 255),(228, 228, 228),(136, 136, 136),(34, 34, 34),(255, 167, 209),(229, 0, 0),(229, 149, 0),(160, 106, 66),(229, 217, 0),(148, 224, 68),(2, 190, 1),(0, 211, 221),(0, 131, 199),(0, 0, 234),(207, 110, 228),(130, 0, 128)]

def getBigChunk(x, y,):
	result = r = requests.get('http://pixelcanvas.io/api/bigchunk/{}.{}.bmp'.format(x,y))
	return result.content

BLOCK_SIZE = 64
RADIUS = 7
BLOCKS = 7
SIZE = BLOCKS * (BLOCK_SIZE * RADIUS + BLOCK_SIZE + BLOCK_SIZE * RADIUS)
OFFSET = (SIZE - BLOCK_SIZE) / 2

while 1:
	try:
		deltaT = time()
		name = strftime("%j-%H%M%S")
		print("generating img {}".format(name))
		img = Image.new('RGB', (SIZE, SIZE), (255, 255, 255))
		pix = img.load()
		for center_x in [-45,-30,-15,0,15,30,45]:
			for center_y in  [-45,-30,-15,0,15,30,45]:
				raw_data = getBigChunk(center_x,center_y)
				current_byte = 0

				for bigchunk_y in range(center_y-RADIUS,center_y+RADIUS+1):
					for bigchunk_x in range(center_x-RADIUS,center_x+RADIUS+1):
						for block_y in range(BLOCK_SIZE):
							current_y = bigchunk_y * BLOCK_SIZE + block_y
							for block_x in range(0,BLOCK_SIZE,2):
								current_x = bigchunk_x * BLOCK_SIZE + block_x
								pix[current_x + OFFSET, current_y + OFFSET] = colors[raw_data[current_byte] >> 4]
								pix[current_x+1  + OFFSET, current_y + OFFSET] = colors[raw_data[current_byte] & 0x0F]
								current_byte += 1
		img.save("timelapse-300s/{}.png".format(name))
		print("img {} saved.".format(name))
		while time()-deltaT<300:
			sleep(5)
	except:
		print("Error, retrying in 10 seconds...")
		sleep(10)
