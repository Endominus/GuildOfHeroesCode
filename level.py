from entities import *
from dialog import *
import sprites

class Level(object):

	def __init__(self, source, assets):
		self.frm, allsprites_list, obstacles_list = sprites.load_level_data(source, assets)
		self.player = Player_Character('ghost_ss.bmp', self.frm)
		allsprites_list.append(self.player)
		self.allsprites = pygame.sprite.LayeredUpdates(allsprites_list)
		self.NPCs = pygame.sprite.LayeredUpdates()
		self.obstacles = pygame.sprite.Group(obstacles_list)
		self.frm.obstruct(self.player, self.obstacles)
		self.dT = DialogTree()
		self.events = dict()
		self.event_triggers = []
		self.proximity_triggers = []
		
	def add_npc(self, image, x_loc, y_loc, rel):
		actor = NPC(image, x_loc, y_loc, self.frm)
		actor.layer = 3
		actor.interactive = True
		actor.relationship = rel
		
		self.allsprites.add(actor)
		self.obstacles.add(actor)
		self.NPCs.add(actor)
		return actor
		
	def add_events_dict(self, keys, values):
		self.events = dict(zip(keys, values))
		
	def add_event_trigger(self, trigger, type, vals):
		e = EventTrigger(trigger, type, vals)
		self.event_triggers.append(e)
		
	def add_proximity_trigger(self, loc_data, triggers, keys, unstable):
		if type(loc_data) == list:
			p = ProximityTrigger(loc_data[0], loc_data[1], loc_data[2], triggers, keys, unstable)
		else:
			p = ProximityTrigger([0, 0], 0, 0, triggers, keys, unstable)
			p.link_object(loc_data)
		self.proximity_triggers.append(p)
		
	def add_dialog_node(self, id, MCSwitch, attributes):
		self.dT.addNode(id, MCSwitch, attributes)
		
		
		
def load_level(level_name):
	if level_name == "prologue_outside":
		level = Level('prologue_outside.txt', 1)
		medic = level.add_npc('Medic.bmp', 500, 500, 20)
		level.add_events_dict(['prologue_near_medic'], [False, False])
		level.add_proximity_trigger(medic, [], [['prologue_near_medic', True]], True)
		level.add_event_trigger(['prologue_near_medic', 'action_button'], 0, ['0', medic])
		level.add_dialog_node("0", 0, ["First node", "Medic", 0, 0, [], 0, 0, False])
		level.add_dialog_node("0.0", 0, ["Second node", "Ghost", 0, 0, [], 0, 0, False])
		level.add_dialog_node("0.0.0", True, [[0, 100], [0, 100], [0, 100], [0, 100], [0, 100], [], "A choice", ["I made the good choice. Yay!", "Ghost", 0, 0, [], 0, 0, True]])
		level.add_dialog_node("0.0.1", True, [[0, 100], [0, 100], [0, 100], [0, 100], [0, 100], [], "Another choice", ["I made the bad choice. Boo!", "Ghost", 0, 0, [], 0, 0, True]])
		
		return level