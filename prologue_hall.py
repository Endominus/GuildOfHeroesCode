from entities import *
from dialog import *
import sprites

def initialize_level():
	frm, allsprites_list, obstacles_list = sprites.load_level_data('prologue_outside.txt', 1)
	player = Player_Character('ghost_ss.bmp', frm)
	allsprites_list.append(player)
	allsprites = pygame.sprite.LayeredUpdates(allsprites_list)
	NPCs = pygame.sprite.LayeredUpdates()
	obstacles = pygame.sprite.Group(obstacles_list)
	frm.obstruct(player, obstacles)
	
	actor = NPC('Medic.bmp', 500, 500, frm)
	actor.layer = 3
	actor.interactive = True
	actor.relationship = 20
	actor.interaction_type = "conversation"
	#actor.interaction = Simple_Conversation(["Hello.", "I'm a person!", "I think you're a person too.", "Sometimes I say things...", "things!", "That wasn't really approriate, was it?", "When I said \"I say things\", I didn't quote it. Its almost like cheating.", "Here, I'll try again.", "Sometimes I say \"Things\".", "Things.", "It didn't really work the second time, did it?", "Anyway, you can't go away until I stop talking, can you?", "Hah, that'll teach you to explore.", "Trying to be all immersion'd and whatnot.", "Learn about the games backstory and world.", "You would, wouldn't you.", "Well listen here sonny!", "I'm on to you. So y'alls best watch out now.", "Or I'll...er...", "THINGS!", "(ninja poof)", "(you can't see me anymore)", "(go away)" ], 0, 0)
	actor.set_seed('0')

#	nextLv = Obstacle('Medic.bmp', 400, 400, frm)
#	nextLv.layer = 3
#	nextLv.interactive = True
#	nextLv.interaction_type = "level"
#	nextLv.interaction = prologue_hall

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
