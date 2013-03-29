from entities import *
import sprites

def initialize_level():
	frm, allsprites_list, obstacles_list = sprites.load_level_data('prologue_outside.txt', 1)
	player = Player_Character('ghost_ss.bmp', frm)
	allsprites_list.append(player)
	allsprites = pygame.sprite.LayeredUpdates(allsprites_list)
	obstacles = pygame.sprite.Group(obstacles_list)
	frm.obstruct(player, obstacles)
	
	actor = Obstacle('Medic.bmp', 500, 500, frm)
	actor.layer = 3
	actor.interactive = True
	actor.interaction = Simple_Conversation(["Hello.", "I'm a person!", "I think you're a person too.", "Sometimes I say things...", "things!", "That wasn't really approriate, was it?", "When I said \"I say things\", I didn't quote it. Its almost like cheating.", "Here, I'll try again.", "Sometimes I say \"Things\".", "Things.", "It didn't really work the second time, did it?", "Anyway, you can't go away until I stop talking, can you?", "Hah, that'll teach you to explore.", "Trying to be all immersion'd and whatnot.", "Learn about the games backstory and world.", "You would, wouldn't you.", "Well listen here sonny!", "I'm on to you. So y'alls best watch out now.", "Or I'll...er...", "THINGS!", "(ninja poof)", "(you can't see me anymore)", "(go away)" ], 0, 0)

	allsprites.add(actor)
	obstacles.add(actor)

	interactables = pygame.sprite.Group(actor)

	return frm, player, interactables, allsprites
