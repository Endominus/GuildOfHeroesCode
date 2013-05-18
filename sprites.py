import os
from entities import *

sprite_dictionary_1 = {'a': "tile_floor.bmp", 'b': "bottom_sidewalk_temp.bmp", 'c': ".bmp", 'd': "left_door_temp.bmp", 'e': "building_exterior.bmp", 'f': ".bmp", 'g': ".bmp", 'h': ".bmp", 'i': ".bmp", 'j': ".bmp", 'k': ".bmp", 'l': ".bmp", 'm': ".bmp", 'n': ".bmp", 'o': ".bmp", 'p': ".bmp", 'q': ".bmp", 'r': ".bmp", 's': "sidewalk_temp.bmp", 't': "top_sidewalk_temp.bmp", 'u': ".bmp", 'v': ".bmp", 'w': "window_temp.bmp", 'x': ".bmp", 'y': ".bmp", 'z': ".bmp", 'A': ".bmp", 'B': "banner_temp.bmp", 'C': ".bmp", 'D': "right_door_temp.bmp", 'E': ".bmp", 'F': ".bmp", 'G': ".bmp", 'H': ".bmp", 'I': ".bmp", 'J': ".bmp", 'K': ".bmp", 'L': "street_lines_temp.bmp", 'M': ".bmp", 'N': ".bmp", 'O': ".bmp", 'P': ".bmp", 'Q': ".bmp", 'R': ".bmp", 'S': "street.bmp", 'T': "trophy_template.bmp", 'U': ".bmp", 'V': "wall_temp.bmp", 'W': ".bmp", 'X': ".bmp", 'Y': ".bmp", 'Z': "north_wall.bmp"}

sprite_dictionary_2 = {'a': "tile_floor.bmp", 'b': ".bmp", 'c': ".bmp", 'd': "left_door_temp.bmp", 'e': "street.bmp", 'f': "nw_corner.bmp", 'g': "north_wall.bmp", 'h': "ne_corner.bmp", 'i': "left_wall.bmp", 'j': "se_corner.bmp", 'k': "south_wall.bmp", 'l': "sw_corner.bmp", 'm': "right_wall.bmp", 'n': "nw_uncorner.bmp", 'o': "north_uncorner.bmp", 'p': "ne_uncorner.bmp", 'q': "north_p_wall.bmp", 'r': "east_uncorner.bmp", 's': "east_p_wall.bmp", 't': "se_uncorner.bmp", 'u': "south_uncorner.bmp", 'v': "sw_uncorner.bmp", 'w': "south_p_wall.bmp", 'x': "west_uncorner.bmp", 'y': "west_p_wall.bmp", 'z': ".bmp", 'A': ".bmp", 'B': ".bmp", 'C': ".bmp", 'D': "right_door_temp.bmp", 'E': ".bmp", 'F': ".bmp", 'G': ".bmp", 'H': ".bmp", 'I': ".bmp", 'J': ".bmp", 'K': ".bmp", 'L': "street_lines_temp.bmp", 'M': ".bmp", 'N': ".bmp", 'O': ".bmp", 'P': ".bmp", 'Q': ".bmp", 'R': ".bmp", 'S': "street.bmp", 'T': "trophy_template.bmp", 'U': ".bmp", 'V': "wall_temp.bmp", 'W': ".bmp", 'X': ".bmp", 'Y': ".bmp", 'Z': ".bmp"}

def load_level_data(level_file, sprite_sheet):
	fullname = os.path.join('data', level_file)
	f = open(fullname, 'r')
	#May be extended for more sprites
	if sprite_sheet == 1:
		spr_dict = sprite_dictionary_1
	elif sprite_sheet == 2:
		spr_dict = sprite_dictionary_2
	line = f.readline()
	#Coordinates
	x, y = 0, 0
	width = 0
	height = 0
	#Image
	sprite_name = ""
	#Frame
	frm = Frame()
	#frm.bind(-20*32, 20*32, -15*32, 15*32)
	#Returning items
	allsprites = []
	obstacles = []
	#Loop exit flag
	quit = False
	#While not at end of file, read background
	while line != "" and not quit:
		#Indicates end of line, need to restart at next line
		for c in line:
			if c == '\n':
				continue
			elif c == '~':
				x, y = 0, -1
				quit = True
				break
			if c != ' ':
				sprite_name = spr_dict[c]
			obs = Obstacle(sprite_name, x*SPRITE_WIDTH, y*SPRITE_HEIGHT, frm, False)
			obs.passable = True
			allsprites.append(obs)
			x += 1
		x = 0
		y += 1
		line = f.readline()
	#While not at end of file, read obstacles
	quit = False
	while line != "" and not quit:
		#Indicates end of line, need to restart at next line
		for c in line:
			if c == '\n':
				break
			elif c == '~':
				x += 1
				continue
			elif c == '`':
				quit = True
				break
			if c != ' ':
				sprite_name = spr_dict[c]
			obs = Obstacle(sprite_name, x*SPRITE_WIDTH, y*SPRITE_HEIGHT, frm, False)
			allsprites.append(obs)
			obstacles.append(obs)
			x += 1
		width = max(width, x)
		x = 0
		y += 1
		height = y
		line = f.readline()

	#frm.bind(-width*16, width*16, -height*16, height*16)
	return frm, allsprites, obstacles
		
	
