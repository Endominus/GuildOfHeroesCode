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
		
	def add_animated_npc(self, image, loc, sizes, rel, id, frames):
		actor = AnimatedNPC(image, loc, sizes, self.frm, id, frames)
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
		#follower = level.add_npc('Medic.bmp', 1200, 1200, 0, 2)
		#follower.movement_target = level.player
		#follower.gs = level.gs
		lucca = level.add_animated_npc('Lucca_ss.bmp', [1200, 1000], [16, 32], 50, 2, [6, 3])
		
		level.add_events_dict(['prologue_near_medic', 'prologue_near_door'], [False, False])
		
		level.add_proximity_trigger(medic, [], [['prologue_near_medic', True]], True)
		level.add_proximity_trigger([[18*SPRITE_WIDTH, 8*SPRITE_HEIGHT], 2*SPRITE_WIDTH, SPRITE_HEIGHT+10], [], [['prologue_near_door', True]], True)
		
		level.add_event_trigger(['prologue_near_medic', 'action_button'], 0, ['0', medic])
		level.add_event_trigger(['prologue_near_door', 'action_button'], 1, 'prologue_hall')
		
		level.add_dialog_node("0", 0, ["First node", "Medic", 0, 0, [], 0, False])
		level.add_dialog_node("0.0", 0, ["Second node", "Ghost", 0, 0, [], 0, False])
		level.add_dialog_node("0.0.0", True, [[[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]], [], "A choice", [100, -1, -1, -1, -1], ["I made the good choice. Yay!", "Ghost", 0, 0, [], 0, True]])
		level.add_dialog_node("0.0.1", True, [[[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]], [], "Another choice", [-1, -1, -1, -1, 0], ["I made the bad choice. Boo!", "Ghost", 0, 0, [], 0, True]])
		
		return level
	elif level_name == "prologue_hall":
		level = Level('prologue_hall.txt', 1, gs)
		level.adjust_starting_pos(-DISTANCE_TO_CENTER_X, -DISTANCE_TO_CENTER_Y)
		level.adjust_starting_pos(13*SPRITE_WIDTH+14, 30*SPRITE_HEIGHT+20)

		stealth_npc = level.add_npc('Medic.bmp', 500, 500, 20, 1)
		mad_dog = level.add_npc('Magus.bmp', 600, 540, 30, 1)
		trophy1 = level.add_npc('trophy_template.bmp', 10*SPRITE_WIDTH, 19*SPRITE_HEIGHT, 1, 1)
		trophy2 = level.add_npc('trophy_template.bmp', 10*SPRITE_WIDTH, 23*SPRITE_HEIGHT, 1, 1)
		trophy3 = level.add_npc('trophy_template.bmp', 10*SPRITE_WIDTH, 27*SPRITE_HEIGHT, 1, 1)
		trophy4 = level.add_npc('trophy_template.bmp', 16*SPRITE_WIDTH, 19*SPRITE_HEIGHT, 1, 1)
		trophy5 = level.add_npc('trophy_template.bmp', 16*SPRITE_WIDTH, 23*SPRITE_HEIGHT, 1, 1)
		trophy6 = level.add_npc('trophy_template.bmp', 16*SPRITE_WIDTH, 27*SPRITE_HEIGHT, 1, 1)
		
		level.add_events_dict(['prologue_near_stealther', 'prologue_near_mad_dog', 'talked_to_mad_dog', 'near_trophy1', 'near_trophy2', 'near_trophy3', 'near_trophy4', 'near_trophy5', 'near_trophy6'], [False, False, False, False, False, False, False, False, False])
		
		level.add_proximity_trigger(stealth_npc, [], [['prologue_near_stealther', True]], True)
		level.add_proximity_trigger(trophy1, [], [['near_trophy1', True]], True)
		level.add_proximity_trigger(trophy2, [], [['near_trophy2', True]], True)
		level.add_proximity_trigger(trophy3, [], [['near_trophy3', True]], True)
		level.add_proximity_trigger(trophy4, [], [['near_trophy4', True]], True)
		level.add_proximity_trigger(trophy5, [], [['near_trophy5', True]], True)
		level.add_proximity_trigger(trophy6, [], [['near_trophy6', True]], True)
		level.add_proximity_trigger(mad_dog, [], [['prologue_near_mad_dog', True]], True)
		
		level.add_event_trigger(['prologue_near_stealther', 'action_button'], 1, 'prologue_stealth')
		level.add_event_trigger(['prologue_near_mad_dog', 'action_button'], 0, ['0', mad_dog])
		level.add_event_trigger(['near_trophy1', 'action_button'], 0, ['1', trophy1])
		level.add_event_trigger(['near_trophy2', 'action_button'], 0, ['2', trophy2])
		level.add_event_trigger(['near_trophy3', 'action_button'], 0, ['3', trophy3])
		level.add_event_trigger(['near_trophy4', 'action_button'], 0, ['4', trophy4])
		level.add_event_trigger(['near_trophy5', 'action_button'], 0, ['5', trophy5])
		level.add_event_trigger(['near_trophy6', 'action_button'], 0, ['6', trophy6])
		level.add_event_trigger(['prologue_near_mad_dog', 'action_button'], 2, [['talked_to_mad_dog'], [True]])
		
		level.add_dialog_node("0", False, ["Who are you?", "Shay de Morta", 0, 0, [], 0, 0, False])
		level.add_dialog_node("0.0", False, ["Huh? What? Oh, I'm just a tourist. Minding my own business, as you can see.", "Trustworthy Fellow", 0, 0, [], 0, 0, False])
		
		level.add_dialog_node("0.0.0", True, [[[0, 100], [0, 100], [0, 100], [0, 80], [30, 100]], [], "He doesn't look like a tourist...", [-1, -1, -1, 40, 60], ["Really? Because you look more like a supervillain.", "Shay de Morta", 0, 0, [], -5, False]])
		level.add_dialog_node("0.0.0.0", False, ["Uh...", "Possible Supervillain", 0, 0, [], 0, False])
		level.add_dialog_node("0.0.0.0.0", False, ["Oh, I get it. You're a cosplayer, aren't you? I read about you guys on the Internet. You go around dressed like your favorite bad guy, right?", "Shay de Morta", 0, 0, [], 0, False])
		level.add_dialog_node("0.0.0.0.0.0", False, ["That's right! I came here dressed as the dreaded villain, Anghamar. But I'm not him. Just acting.", "Just a cosplayer", 0, 0, [], 0, False])
		level.add_dialog_node("0.0.0.0.0.0.0", False, ["Huh, I've never heard of Anghamar. He must be pretty small-time. Well, I 'll leave you to it, then.", "Shay de Morta", 0, 0, [], -10, True])
		
		level.add_dialog_node("0.0.1", True, [[[30, 100], [0, 100], [0, 100], [50, 100], [0, 100]], [], "Cool, another superhero nerd!", [60, -1, 55, 70, -1], ["You're a tourist? I just got here myself, though I wanted to come for years. Isn't this place awesome? Have you seen all the trophies they have?", "Shay de Morta", 0, 0, [], -5, False]])
		level.add_dialog_node("0.0.1.0", False, ["Yes. I've seen the... trophies. They are very nice testaments to the Guild's... effectiveness in battle.", "Not Suspicious At All", 0, 0, [], 0, False])
		
		level.add_dialog_node("0.0.1.0.0", True, [[[30, 100], [40, 100], [40, 100], [0, 100], [0, 100]], [], "Not just in battle!", [-1, 60, 70, -1, -1], ["Hey, the Guild of Heroes is more than a group of people punching out bad guys, you know. They have a really active charitable arm and stuff. You should read this book I've got here by Paragon, \'The Vanguard of Righteousness.\' It talks about how great the Guild is for the country and stuff.", "Shay de Morta", 0, 0, [], -20, False]])
		level.add_dialog_node("0.0.1.0.0.0", False, ["Trust me, I've read the book. I did not come away from it as... enchanted as you clearly were. Now if you would excuse me, I really must get back to observing the area.", "Clearly In It For the Punches", 0, 0, [], 0, False])
		level.add_dialog_node("0.0.1.0.0.0.0", False, ["Whatever, dude. Suit yourself.", "Shay de Morta", 0, 0, [], 0, True])
		
		level.add_dialog_node("0.0.1.0.1", True, [[[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]], [], "That sounded kinda suspicious.", [-1, -1, -1, -1, -1], ["Do you have some kinda problem with the Guild? Like those people outside?", "Shay de Morta", 0, 0, [], 5, False]])
		level.add_dialog_node("0.0.1.0.1.0", False, ["No, not like those people. They want to join the Guild. I... do not. Please, go. I have wasted enough time speaking to you.", "Definitely A Creep", 0, 0, [], 0, True])
		
		level.add_dialog_node("1", False, ["This is the trophy President O'Harra gave to Paragon for saving New Las Vegas from the Moon-Martians of Neptune! I can't believe people thought that was faked.", "Shay de Morta", 0, 0, [], 0, False])
		level.add_dialog_node("1.0", True, [[[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]], [], "Maybe it was...", [0, 1, 0, -2, 2], ["Then again, it could have been. I mean, no one but Paragon ever saw them. He said that they were invisible, and I suppose Moon-Martians would be.", "Shay de Morta", 0, 0, [], 0, True]])
		level.add_dialog_node("1.1", True, [[[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]], [], "But it couldn't have been.", [0, -1, 0, 2, -2], ["But he's a hero, and he wouldn't lie. Anyway, the government said they recovered evidence of the alien spacecraft, whatever nuts on the Internet might say.", "Shay de Morta", 0, 0, [], 0, True]])
		
		level.add_dialog_node("2", False, ["I didn't know the Leadbelter and Velvet Glove saved Panama! I thought they stayed more towards the Canadian border, just in case.", "Shay de Morta", 0, 0, [], 0, False])
		level.add_dialog_node("2.0", False, ["Oh, wait, this says they saved Panama, Illinois. That's... huh.", "Shay de Morta", 0, 0, [], 0, False])
		level.add_dialog_node("2.0.0", True, [[[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]], [], "Are they trying to make themselves look good?", [0, 1, 0, -2, 0], ["The fine print there makes them kinda look like they're saying the saved the country. That's a little cheap.", "Shay de Morta", 0, 0, [], 0, True]])
		level.add_dialog_node("2.0.1", True, [[[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]], [], "It's something...", [0, 0, 0, 3, -1], ["Hey, they can't all be world-shaking heroics. They were there for Panama when no one else was, I guess.", "Shay de Morta", 0, 0, [], 0, True]])
		level.add_dialog_node("2.0.2", True, [[[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]], [], "That's not that heroic.", [0, -5, 0, -2, 1], ["What, the National Guard couldn't handle that? Heroes are supposed to be larger than life, trotting around the globe, saving millions. That's a real let down.", "Shay de Morta", 0, 0, [], 0, True]])
		
		level.add_dialog_node("3", False, ["\'Awarded to Crovax, from the people of Atlanta.\' Crovax, Crovax... He's the guy who shoots bees out of his mouth, right? Ugh, I hate bees.", "Shay de Morta", 0, 0, [], 0, False])
		level.add_dialog_node("3.0", False, ["I guess this was when the Atlanteans attacked Georgia. That was a real bummer. Mom canceled our vacation there and everything. I could have seen the Guild helping out in person.", "Shay de Morta", 0, 0, [], 0, False])
		level.add_dialog_node("3.0.0", True, [[[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]], [], "She was totally overreacting.", [0, 0, 0, 0, -2], ["I don't care what anyone says, Crovax did good work in Georgia. So some people got hurt. That's what happens when you defend the homeland, right?", "Shay de Morta", 0, 0, [], 0, True]])
		level.add_dialog_node("3.0.1", True, [[[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]], [], "Shame what happened to those people.", [0, 2, 1, 0, 2], ["Maybe Crovax wasn't the best choice to defend some place. I heard a lot of people there were killed by bee swarms before they all got cleared out. What a mess that was.", "Shay de Morta", 0, 0, [], 0, True]])
		
		level.add_dialog_node("4", False, ["\'Awarded to the true patriots who helped defeat secessionists in our midst.\' I remember when South Carolina tried to secede. It was a plot by the Union of Evil, right?", "Shay de Morta", 0, 0, [], 0, False])
		level.add_dialog_node("4.0", True, [[[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]], [], "No, it wasn't...", [0, 0, 0, 0, 0], ["No, wait, they found out later that some people there actually did want to secede. Honestly, though, the Union only have themselves to blame when they have such a terrible title.", "Shay de Morta", 0, 0, [], 0, True]])
		level.add_dialog_node("4.1", True, [[[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]], [], "Damn Unionists.", [0, -1, 0, -2, 2], ["I don't see why the government even lets them stay around. I mean, we know where the bad guys are, right? Why not just arrest them all?", "Shay de Morta", 0, 0, [], 0, True]])
		
		level.add_dialog_node("5", False, ["\'New York Department of Food  and Safety Inspections Rating: B+.\' Well, that\'s nice.", "Shay de Morta", 0, 0, [], 0, False])
		level.add_dialog_node("5.0", False, ["Wait, how'd they get a trophy made out of this? Does the sanitation department just give out trophies now?", "Shay de Morta", 0, 0, [], 0, True])
		
		level.add_dialog_node("6", False, ["'In Memoriam; To all those who gave their lives to stop the tyranny of the Septemberists, and the martyrs of May 6th, 1992. Your sacrifice will always be remembered.'", "Shay de Morta", 0, 0, [], 0, False])
		level.add_dialog_node("6.0", True, [[[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]], [], "If only we could put the war behind us.", [0, 3, 1, 2, -1], ["The sooner the world moves past the Succession, the better it will be for everyone. There's been enough fighting over who controls what. The world can't afford another war like that one.", "Shay de Morta", 0, 0, [], 0, True]])
		level.add_dialog_node("6.1", True, [[[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]], [], "We will never forget", [0, 1, -1, -2, 1], ["One day we'll pay them back. It won't bring anyone back, but it's wrong to just walk away like they meant nothing. Maybe we couldn't have done anything then, but now...", "Shay de Morta", 0, 0, [], 0, True]])
		
		# level.add_dialog_node("", False, ["", "", 0, , [], , False])
		# level.add_dialog_node("", True, [[[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]], [], "", [0, 0, 0, 0, 0], ["", "Shay de Morta", 0, 0, [], 0, False]])
		
		return level
	elif level_name == 'prologue_stealth':
		level = Level('prologue_stealth.txt', 1, gs)
		level.adjust_starting_pos(-DISTANCE_TO_CENTER_X, -DISTANCE_TO_CENTER_Y)
		level.adjust_starting_pos(38*SPRITE_WIDTH+14, 20*SPRITE_HEIGHT+20)

		guards_positions = ((5,18), (5, 38), (6, 3), (14, 6), (6, 23), (21, 4), (23, 5), (21, 17))
		guards_paths = (0, 
		    0,#((5,38), (2, 38), (2, 30), (2, 38)),
		    0,#((6, 3), (10, 8)),
		    #((adjx(14) ,adjy(6)), (adjx(9), adjy(6))),
		    ((adjx(1), adjy(1)), (adjx(10), adjy(1))),
		    0,#((6, 23), (12, 33)),
		    0,
		    0,#((adjx(23), adjy(5)), (adjx(19), adjy(21))),
		    0)
		i = 0
		for n in guards_positions:
		    guard = level.add_npc('Medic.bmp', SPRITE_WIDTH*(n[1]-1), SPRITE_HEIGHT*(n[0]-1), 20, 1)
		    guard.guard_behavior = True
		    guard.AI_behavior = "guard"
		    guard.AI_guard_target = level.player
		    guard.movement_target = level.player
		    guard.gs = level.gs
		    guard.AI_patrol_route = guards_paths[i]
		    i+=1

		cat = level.add_npc('Pascal.png',250, 250, 20, 1)
		cat.AI_behavior = "cat"
		cat.AI_cat_target = level.player
		cat.gs = level.gs

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

def adjx(x):
    return (x)*SPRITE_WIDTH
def adjy(y):
    return (y)*SPRITE_HEIGHT
