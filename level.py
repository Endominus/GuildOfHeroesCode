from entities import *
from dialog import *
import sprites

class Level(object):

	def __init__(self, source, assets):
		self.frm, self.allsprites_list, self.obstacles_list = sprites.load_level_data(source, assets)
		self.player = Player_Character('ghost_ss.bmp', self.frm)
		self.allsprites_list.append(player)
		self.allsprites = pygame.sprite.LayeredUpdates(allsprites_list)
		self.NPCs = pygame.sprite.LayeredUpdates()
		self.obstacles = pygame.sprite.Group(self.obstacles_list)
		self.frm.obstruct(self.player, self.obstacles)
		self.dT = DialogTree()
		self.interactables = pygame.sprite.Group()
		self.events = dict()
		
	def add_npc(self, image, x_loc, y_loc, rel, seed):
		actor = NPC(image, x_loc, y_loc, self.frm)
		actor.layer = 3
		actor.interactive = True
		actor.relationship = rel
		actor.set_seed(seed)
		
		self.allsprites.add(actor)
		self.obstacles.add(actor)
		self.NPCs.add(actor)
		self.interactables.add(actor)
		
	def add_events_dict(self, keys, values):
		self.events = dict(zip(keys, values))