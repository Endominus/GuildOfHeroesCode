from entities import *
from dialog import *
import sprites


#So, this file doesn't do anything anymore?
def initialize_level():
	frm, allsprites_list, obstacles_list = sprites.load_level_data('prologue_hall.txt', 1)
	frm.x = 0#(32*12)
	frm.y = 0#(32*35)
	player = Player_Character('ghost_ss.bmp', frm)
	allsprites_list.append(player)
	allsprites = pygame.sprite.LayeredUpdates(allsprites_list)
	NPCs = pygame.sprite.LayeredUpdates()
	obstacles = pygame.sprite.Group(obstacles_list)
	frm.obstruct(player, obstacles)
	
	actor = NPC('Medic.bmp', 490, 500, frm)
	actor.layer = 3
	actor.interactive = True
	actor.relationship = 20
	actor.interaction_type = "conversation"
	actor.set_seed('0')

	dT = DialogTree()
	dT.addNode("0", 0, ["First node", "Medic", 0, 0, [], 0, 0, False])
	dT.addNode("0.0", 0, ["Second node", "Ghost", 0, 0, [], 0, 0, True])
	
	
	allsprites.add(actor)
	obstacles.add(actor)
	NPCs.add(actor)

#	allsprites.add(nextLv)
#	obstacles.add(nextLv)

	interactables = pygame.sprite.Group(actor)
#	interactables.add(nextLv)

	return frm, player, interactables, allsprites, NPCs, dT
