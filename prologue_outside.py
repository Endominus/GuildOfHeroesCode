from entities import *
from dialog import *
import sprites
import prologue_hall

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
	actor.change_facing(0)
	
	actor1 = NPC('Medic.bmp', 700, 500, frm)
	actor1.layer = 3
	actor1.interactive = True
	actor1.change_facing(1)
	
	actor2 = NPC('Medic.bmp', 900, 500, frm)
	actor2.layer = 3
	actor2.interactive = True
	actor2.change_facing(2)
	
	actor3 = NPC('Medic.bmp', 1100, 500, frm)
	actor3.layer = 3
	actor3.interactive = True
	actor3.change_facing(3)

	# nextLv = Obstacle('Medic.bmp', 400, 400, frm)
	# nextLv.layer = 3
	# nextLv.interactive = True
	# nextLv.interaction_type = "level"
	# nextLv.interaction = prologue_hall
	
	lldoor = Obstacle("left_door_temp.bmp", 512, 256, frm, False)
	lldoor.layer = 3
	lldoor.interactive = True
	lldoor.interaction_type = "level"
	lldoor.interaction = prologue_hall
	
	lrdoor = Obstacle("right_door_temp.bmp", 544, 256, frm, False)
	lrdoor.layer = 3
	lrdoor.interactive = True
	lrdoor.interaction_type = "level"
	lrdoor.interaction = prologue_hall
	
	rldoor = Obstacle("left_door_temp.bmp", 640, 256, frm, False)
	rldoor.layer = 3
	rldoor.interactive = True
	rldoor.interaction_type = "level"
	rldoor.interaction = prologue_hall
	
	rrdoor = Obstacle("right_door_temp.bmp", 672, 256, frm, False)
	rrdoor.layer = 3
	rrdoor.interactive = True
	rrdoor.interaction_type = "level"
	rrdoor.interaction = prologue_hall

	dT = DialogTree()
	dT.addNode("0", 0, ["First node", "Medic", 0, 0, [], 0, 0, False])
	dT.addNode("0.0", 0, ["Second node", "Ghost", 0, 0, [], 0, 0, False])
	dT.addNode("0.0.0", True, [[0, 100], [0, 100], [0, 100], [0, 100], [0, 100], [], "A choice", ["I made the good choice. Yay!", "Ghost", 0, 0, [], 0, 0, True]])
	dT.addNode("0.0.1", True, [[0, 100], [0, 100], [0, 100], [0, 100], [0, 100], [], "Another choice", ["I made the bad choice. Boo!", "Ghost", 0, 0, [], 0, 0, True]])
	
	
	allsprites.add(actor)
	obstacles.add(actor)
	NPCs.add(actor)
	NPCs.add(actor1)
	allsprites.add(actor1)
	obstacles.add(actor1)
	
	NPCs.add(actor2)
	allsprites.add(actor2)
	obstacles.add(actor2)
	
	NPCs.add(actor3)
	allsprites.add(actor3)
	obstacles.add(actor3)

	# allsprites.add(nextLv)
	# obstacles.add(nextLv)
	allsprites.add(lldoor)
	obstacles.add(lldoor)
	allsprites.add(rldoor)
	obstacles.add(rldoor)
	allsprites.add(rrdoor)
	obstacles.add(rrdoor)
	allsprites.add(lrdoor)
	obstacles.add(lrdoor)

	interactables = pygame.sprite.Group(actor)
	#interactables.add(nextLv)
	interactables.add(lldoor)
	interactables.add(rldoor)
	interactables.add(lrdoor)
	interactables.add(rrdoor)

	return frm, player, interactables, allsprites, NPCs, dT
