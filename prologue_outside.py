from entities import *
import sprites

def initialize_level():
	frm, allsprites_list, obstacles_list = sprites.load_level_data('prologue_outside.txt', 1)
	player = Player_Character('Ghost.bmp', frm)
	allsprites_list.append(player)
	allsprites = pygame.sprite.LayeredUpdates(allsprites_list)
	obstacles = pygame.sprite.Group(obstacles_list)
	frm.obstruct(player, obstacles)
	
	actor = Obstacle('Ghost.bmp', 500, 500, frm)
	actor.layer = 3
	allsprites.add(actor)
	obstacles.add(actor)

	interactables = pygame.sprite.Group(actor)

	player.make_interact(interactables)

	return frm, allsprites
