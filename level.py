from entities import *
from dialog import *
import sprites

DISTANCE_TO_CENTER_X = 8*SPRITE_WIDTH-14
DISTANCE_TO_CENTER_Y = 5*SPRITE_HEIGHT-20

class Level(object):

	def __init__(self, source, assets, gs):
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
		self.gs = gs
		
	def add_npc(self, image, x_loc, y_loc, rel, id):
		actor = NPC(image, x_loc, y_loc, self.frm, id)
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
		
	def adjust_starting_pos(self, x, y):
		self.frm.x += x
		self.player.x_pos += x
		self.frm.y += y
		self.player.y_pos += y
		
def load_level(level_name, gs):
	if level_name == "prologue_outside":
		level = Level('prologue_outside.txt', 1, gs)
		level.adjust_starting_pos(-DISTANCE_TO_CENTER_X, -DISTANCE_TO_CENTER_Y)
		level.adjust_starting_pos(18.5*SPRITE_WIDTH+20, 10*SPRITE_HEIGHT+20)
		
		medic = level.add_npc('Medic.bmp', 1000, 1000, 20, 1)
		banner = level.add_npc('banner.bmp', 15.5*SPRITE_WIDTH, 5*SPRITE_HEIGHT, 0, 3)
		follower = level.add_npc('Medic.bmp', 1200, 1200, 0, 2)
		follower.movement_target = level.player
		follower.gs = level.gs
		
		level.add_events_dict(['prologue_near_medic', 'prologue_near_door'], [False, False])
		
		level.add_proximity_trigger(medic, [], [['prologue_near_medic', True]], True)
		level.add_proximity_trigger([[18*SPRITE_WIDTH, 8*SPRITE_HEIGHT], 2*SPRITE_WIDTH, SPRITE_HEIGHT+10], [], [['prologue_near_door', True]], True)
		
		level.add_event_trigger(['prologue_near_medic', 'action_button'], 0, ['0', medic])
		level.add_event_trigger(['prologue_near_door', 'action_button'], 1, 'prologue_hall')
		
		level.add_dialog_node("0", 0, ["First node", "Medic", 0, 0, [], 0, 0, False])
		level.add_dialog_node("0.0", 0, ["Second node", "Ghost", 0, 0, [], 0, 0, False])
		level.add_dialog_node("0.0.0", True, [[0, 100], [0, 100], [0, 100], [0, 100], [0, 100], [], "A choice", [100, -1, -1, -1, -1], ["I made the good choice. Yay!", "Ghost", 0, 0, [], 0, 0, True]])
		level.add_dialog_node("0.0.1", True, [[0, 100], [0, 100], [0, 100], [0, 100], [0, 100], [], "Another choice", [-1, -1, -1, -1, 0], ["I made the bad choice. Boo!", "Ghost", 0, 0, [], 0, 0, True]])
		
		print "Player location:", level.player.x_pos, level.player.y_pos
		return level
	elif level_name == "prologue_hall":
		level = Level('prologue_hall.txt', 1, gs)
		level.adjust_starting_pos(-DISTANCE_TO_CENTER_X, -DISTANCE_TO_CENTER_Y)
		level.adjust_starting_pos(13*SPRITE_WIDTH+14, 30*SPRITE_HEIGHT+20)

		stealth_npc = level.add_npc('Medic.bmp', 500, 500, 20, 1)
		level.add_events_dict(['prologue_near_stealther'], [False])
		level.add_proximity_trigger(stealth_npc, [], [['prologue_near_stealther', True]], True)
		level.add_event_trigger(['prologue_near_stealther', 'action_button'], 1, 'prologue_stealth')
		
		#8, 18
		return level
	elif level_name == 'prologue_stealth':
		level = Level('prologue_stealth.txt', 1, gs)
		level.adjust_starting_pos(-DISTANCE_TO_CENTER_X, -DISTANCE_TO_CENTER_Y)
		level.adjust_starting_pos(38*SPRITE_WIDTH+14, 20*SPRITE_HEIGHT+20)

		guards_positions = ((5,18), (5, 38), (6, 3), (14, 6), (6, 23), (21, 4), (23, 5), (21, 17))

		for n in guards_positions:
		    guard = level.add_npc('Medic.bmp', SPRITE_WIDTH*(n[1]-1), SPRITE_HEIGHT*(n[0]-1), 20, 1)


		return level
	elif level_name == "":
		
		pass
		#Initialize level
		#level = Level('NAME.txt', SPR_SHEET, gs)
		#level.adjust_starting_pos(-DISTANCE_TO_CENTER_X, -DISTANCE_TO_CENTER_Y)
		#level.adjust_starting_pos(x, y)
		
		#Create all NPCs
		
		#Create events_dict
		
		#Add Proximity triggers
		
		#Add Event triggers
		
		#Add Dialog nodes
		
		#return level
