from entities import *
import sprites

def initialize_level():
	frm, allsprites_list, obstacles_list = sprites.load_level_data('prologue_outside.txt', 1)
	player = Player_Character('Ghost.bmp', frm)
	allsprites_list.append(player)
	allsprites = pygame.sprite.LayeredUpdates(allsprites_list)
	obstacles = pygame.sprite.Group(obstacles_list)
	frm.obstruct(player, obstacles)
	
	return frm, allsprites
