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
		
	def add_animated_npc(self, image, loc, sizes, rel, id, frames, facing = 0):
		actor = AnimatedNPC(image, loc, sizes, self.frm, id, frames)
		actor.layer = 3
		actor.interactive = True
		actor.relationship = rel
		actor.facing = facing
		
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
		level = Level('prologue_hall.txt', 2, gs)
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
		
		level.add_events_dict(['prologue_near_stealther', 'prologue_near_mad_dog', 'talked_to_mad_dog', 'talked_to_secretary', 'near_trophy1', 'near_trophy2', 'near_trophy3', 'near_trophy4', 'near_trophy5', 'near_trophy6'], [False, False, False, False, False, False, False, False, False, False])
		
		level.add_proximity_trigger(stealth_npc, [], [['prologue_near_stealther', True]], True)
		level.add_proximity_trigger(trophy1, [], [['near_trophy1', True]], True)
		level.add_proximity_trigger(trophy2, [], [['near_trophy2', True]], True)
		level.add_proximity_trigger(trophy3, [], [['near_trophy3', True]], True)
		level.add_proximity_trigger(trophy4, [], [['near_trophy4', True]], True)
		level.add_proximity_trigger(trophy5, [], [['near_trophy5', True]], True)
		level.add_proximity_trigger(trophy6, [], [['near_trophy6', True]], True)
		level.add_proximity_trigger(mad_dog, [], [['prologue_near_mad_dog', True]], True)
		
		level.add_event_trigger(['talked_to_secretary'], 1, 'prologue_walkaround')
		level.add_event_trigger(['prologue_near_mad_dog', 'action_button'], 0, ['0', mad_dog])
		level.add_event_trigger(['prologue_near_mad_dog', 'action_button'], 2, [['talked_to_mad_dog'], [True]])
		level.add_event_trigger(['near_trophy1', 'action_button'], 0, ['1', trophy1])
		level.add_event_trigger(['near_trophy2', 'action_button'], 0, ['2', trophy2])
		level.add_event_trigger(['near_trophy3', 'action_button'], 0, ['3', trophy3])
		level.add_event_trigger(['near_trophy4', 'action_button'], 0, ['4', trophy4])
		level.add_event_trigger(['near_trophy5', 'action_button'], 0, ['5', trophy5])
		level.add_event_trigger(['near_trophy6', 'action_button'], 0, ['6', trophy6])
		level.add_event_trigger(['prologue_near_stealther', 'action_button'], 2, [['talked_to_secretary'], [True]])
		level.add_event_trigger(['prologue_near_stealther', 'action_button'], 0, ['7', stealth_npc])
		
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
		
		level.add_dialog_node("0.0.1.0.1", True, [[[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]], [], "That sounded kinda suspicious.", [-1, -1, -1, -1, -1], ["Do you have some kinda problem with the Guild? Like those people who protested a couple of weeks ago?", "Shay de Morta", 0, 0, [], 5, False]])
		level.add_dialog_node("0.0.1.0.1.0", False, ["No, not like those people. They want to join the Guild, and have complaints about its progressiveness. I... do not want to join. Please, go. I have wasted enough time speaking to you.", "Definitely A Creep", 0, 0, [], 0, True])
		
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
		
		level.add_dialog_node("7", False, ["Hello! Welcome to the Guild of Heroes meeting hall. Are you here to petition a hero, visit the gift shop, or go for a tour? One just left unfortunately, but they run every hour.", "Secretary", 0, 0, [], 0, False])
		level.add_dialog_node("7.0", False, ["I'm here to join the Guild, actually. My name is Shay de Morta. I called ahead and arranged an appointment...?", "Shay de Morta", 0, 0, [], 0, False])
		level.add_dialog_node("7.0.0", False, ["de Morta, huh? I think I heard of-! You're that person people have been talking about! You possessed one of your classmates, right?", "Secretary", 0, 0, [], 0, False])
		level.add_dialog_node("7.0.0.0", True, [[[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]], [], "It was an accident!", [0, 2, 0, 1, 1], ["I totally didn't mean to! I just panicked and it happened, all right?", "Shay de Morta", 0, 0, [], 0, False]])
		level.add_dialog_node("7.0.0.0.0", False, ["Really? The news would disagree. I don't approve of bullies, you know. I see your name on the list. Please follow me whenever you're ready to go.", "Secretary", 0, 0, [], 0, False])
		level.add_dialog_node("7.0.0.0.0.0", True, [[[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]], [], "Okay", [0, 0, 0, 0, 0], ["Let's go. I don't want to lost my nerve now, after all.", "Shay de Morta", 0, 0, [], 0, True]])
		level.add_dialog_node("7.0.0.0.0.1", True, [[[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]], ['talked_to_mad_dog'], "Actually, about that guy over there...", [0, 0, 0, 0, 0], ["I think that guy over there's up to something. He said some really fishy stuff to me.", "Shay de Morta", 0, 0, [], 0, False]])
		level.add_dialog_node("7.0.0.0.0.1.0", False, ["I'll call security. They can handle him.", "Secretary", 0, 0, [], 0, True])
		
		level.add_dialog_node("7.0.0.1", True, [[[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]], [], "She deserved it.", [2, -1, 0, 0, -1], ["Yeah, but don't let the news reports fool you. I didn't start the fight, I just finished it. If I hadn't done that... well, let's just say she's was never the nicest person.", "Shay de Morta", 0, 0, [], 0, False]])
		level.add_dialog_node("7.0.0.1.0", False, ["Whatever you say. I won't tell anyone; bullies deserve a little reckoning, right? I see your name on the list. Please follow me whenever you're ready to go.", "Secretary", 0, 0, [], 0, False])
		level.add_dialog_node("7.0.0.1.0.0", True, [[[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]], [], "Okay", [0, 0, 0, 0, 0], ["Let's go. I don't want to lost my nerve now, after all.", "Shay de Morta", 0, 0, [], 0, True]])
		level.add_dialog_node("7.0.0.1.0.1", True, [[[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]], ['talked_to_mad_dog'], "Actually, about that guy over there...", [0, 0, 0, 0, 0], ["I think that guy over there's up to something. He said some really fishy stuff to me.", "Shay de Morta", 0, 0, [], 0, False]])
		level.add_dialog_node("7.0.0.1.0.1.0", False, ["I'll call security. They can handle him.", "Secretary", 0, 0, [], 0, True])
		
		
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
	elif level_name == "prologue_walkaround":
		#Initialize level
		level = Level('prologue_walkaround.txt', 2, gs)
		level.adjust_starting_pos(-DISTANCE_TO_CENTER_X, -DISTANCE_TO_CENTER_Y)
		level.adjust_starting_pos(24*SPRITE_WIDTH, 32*SPRITE_HEIGHT)
		
		#Create all NPCs
		ped1 = level.add_npc('pedestal.bmp', 19*SPRITE_WIDTH, 23*SPRITE_HEIGHT, 1, 1)
		ped2 = level.add_npc('pedestal.bmp', 28*SPRITE_WIDTH, 23*SPRITE_HEIGHT, 1, 1)
		ped3 = level.add_npc('pedestal.bmp', 19*SPRITE_WIDTH, 32*SPRITE_HEIGHT, 1, 1)
		ped4 = level.add_npc('pedestal.bmp', 28*SPRITE_WIDTH, 32*SPRITE_HEIGHT, 1, 1)
		ped5 = level.add_npc('pedestal.bmp', 23.5*SPRITE_WIDTH, 26.5*SPRITE_HEIGHT, 1, 1)
		medic = level.add_npc('Medic.bmp', 21*SPRITE_WIDTH, 9*SPRITE_HEIGHT, 1, 1)
		lucca = level.add_animated_npc('Lucca_ss.bmp', [21*SPRITE_WIDTH, 10*SPRITE_HEIGHT], [16, 32], 50, 2, [6, 3], 2)
		
		#Create events_dict
		level.add_events_dict(['near_ped2', 'near_ped3', 'near_ped1', 'near_ped4', 'near_ped5', 'near_chatterers', 'not_eavesdropped_on_chatterers', 'ped1_examined', 'ped2_examined', 'ped3_examined', 'ped5_examined', 'all_peds_examined', 'all_not_peds_examined'], [False, False, False, False, False, False, True, False, False, False, False, False, True])
		
		#Add Proximity triggers
		level.add_proximity_trigger(ped1, [], [['near_ped1', True]], True)
		level.add_proximity_trigger(ped2, [], [['near_ped2', True]], True)
		level.add_proximity_trigger(ped3, [], [['near_ped3', True]], True)
		level.add_proximity_trigger(ped4, [], [['near_ped4', True]], True)
		level.add_proximity_trigger(ped5, [], [['near_ped5', True]], True)
		level.add_proximity_trigger([[22*SPRITE_WIDTH, 10*SPRITE_HEIGHT], SPRITE_WIDTH, 3*SPRITE_HEIGHT], [], [['near_chatterers', True]], False)
		
		#Add Event triggers
		level.add_event_trigger(['near_chatterers', 'not_eavesdropped_on_chatterers'], 0, ['0', lucca])
		level.add_event_trigger(['near_chatterers', 'not_eavesdropped_on_chatterers', 'action_button'], 2, [['not_eavesdropped_on_chatterers'], [False]])
		level.add_event_trigger(['near_ped5', 'action_button'], 0, ['1', lucca])
		level.add_event_trigger(['near_ped1', 'action_button'], 0, ['2', lucca])
		level.add_event_trigger(['near_ped2', 'action_button'], 0, ['3', lucca])
		level.add_event_trigger(['near_ped3', 'action_button'], 0, ['4', lucca])
		level.add_event_trigger(['near_ped4', 'action_button', 'all_not_peds_examined'], 0, ['5', lucca])
		level.add_event_trigger(['near_ped4', 'action_button', 'all_peds_examined'], 0, ['6', lucca])
		level.add_event_trigger(['near_ped1', 'action_button'], 2, [['ped1_examined'], [True]])
		level.add_event_trigger(['near_ped2', 'action_button'], 2, [['ped2_examined'], [True]])
		level.add_event_trigger(['near_ped3', 'action_button'], 2, [['ped3_examined'], [True]])
		level.add_event_trigger(['near_ped5', 'action_button'], 2, [['ped5_examined'], [True]])
		level.add_event_trigger(['ped1_examined', 'ped2_examined', 'ped3_examined', 'ped5_examined'], 2, [['all_peds_examined', 'all_not_peds_examined'], [True, False]])
		
		#Add Dialog nodes
		level.add_dialog_node("0", 0, ["I don't feel comfortable fighting Dr. Octavio anymore. Can you cover Jersey for a couple of weeks while I decompress?", "Scarlet Fever", 0, 0, [], 0, False])
		level.add_dialog_node("0.0", 0, ["Why? What happened?", "Magefire", 0, 0, [], 0, False])
		level.add_dialog_node("0.0.0", 0, ["Last week he was doing his usual thing; you know, 'I am the rightful king of this city, you shall all kneel,' blah blah blah. I show up, tell him we'll never succumb.", "Scarlet Fever", 0, 0, [], 0, False])
		level.add_dialog_node("0.0.0.0", 0, ["Obviously.", "Magefire", 0, 0, [], 0, False])
		level.add_dialog_node("0.0.0.0.0", 0, ["We exchange insults as usual, then he just kind of slumps over.", "Scarlet Fever", 0, 0, [], 0, False])
		level.add_dialog_node("0.0.0.0.0.0", 0, ["A trick? Don't tell me you fell for it.", "Magefire", 0, 0, [], 0, False])
		level.add_dialog_node("0.0.0.0.0.0.0", 0, ["It wasn't a trick. I shot him with an energy blast to make sure. He barely moved. So I go up and ask him what's wrong. He says he's just not feeling the connection any more. That we don't have the same spark.", "Scarlet Fever", 0, 0, [], 0, False])
		level.add_dialog_node("0.0.0.0.0.0.0.0", 0, ["Yikes.", "Magefire", 0, 0, [], 0, False])
		level.add_dialog_node("0.0.0.0.0.0.0.0.0", 0, ["I know, right? This whole time, he thought we were flirting. We get into this huge argument about it, too. Right in front of City Hall! I asked him what he thought of me fighting other villains, then. He tells me he likes a girl who's adventurous. That he's  okay with sharing.", "Scarlet Fever", 0, 0, [], 0, False])
		level.add_dialog_node("0.0.0.0.0.0.0.0.0.0", 0, ["What a creep. Don't worry, you take as long as you need. I'll cover for you until this blows over.", "Magefire", 0, 0, [], 0, True])
		
		level.add_dialog_node("1", False, ["'Paragon is a powerful egotist whose powerset includes flight, invulnerability, super speed, super strength, and rugged good looks. He has no known weaknesses. He has assisted in the capture of many powerful villains, including the Cyclops, Dark Umbrage, and the Moon-Martians of Neptune.'", "Pedestal", 0, 0, [], 0, False])
		level.add_dialog_node("1.0", False, ["'Though his main area of operation is in the heart of our nation, Detroit, he is an international sensation, solving crises in places like Japan, New Zimbabwe, and even the Confederated States of Australia.'", "Pedestal", 0, 0, [], 0, False])
		level.add_dialog_node("1.0.0", False, ["'He is also a well-known and prolific writer, whose works have been translated into seventeen languages. His bestselling series on the life of a modern superhero have both captivated and informed audiences the world over.'", "Pedestal", 0, 0, [], 0, False])
		level.add_dialog_node("1.0.0.0", False, ["'Truly, we can all rest safer in our beds thanks to the tireless vigilance of Paragon.' That's exactly what his trading card says.", "Pedestal", 0, 0, [], 0, False])
		level.add_dialog_node("1.0.0.0.0", True, [[[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]], [], "That was a little much.", [-1, 1, -1, -1, 0], ["That was a little overblown for my tastes. The guy does good work and all, but some humility would be nice. Maybe it was just his biographer writing that stuff.", "Shay de Morta", 0, 0, [], 0, True]])
		level.add_dialog_node("1.0.0.0.1", True, [[[0, 100], [45, 100], [0, 100], [0, 100], [0, 100]], [], "What a hero.", [0, 2, 1, 1, 0], ["That's exactly what the world needs more of. Dedicated people just trying to do good. I'm tired of people just shrugging when I bring this stuff up. These people are moral pillars we could all do to learn something from.", "Shay de Morta", 0, 0, [], 0, True]])
		level.add_dialog_node("1.0.0.0.2", True, [[[0, 100], [0, 100], [0, 100], [0, 100], [45, 100]], [], "Is anyone else terrified of him?", [0, 0, 0, -1, 2], ["This guy kinda terrifies me. What happens if he decides one day that he'd rather rule than serve? I mean, the government says they can stop him, but they haven't really had an opportunity to try. He must have some kind of weakness, right?", "Shay de Morta", 0, 0, [], 0, True]])
		
		level.add_dialog_node("2", False, ["'Vanagoth is a presumably powerful egotist, though his powers have remained as mysterious as he is. While the other members of the Guild of Heroes have credited him with many of their impressive victories, he himself has refused to comment on his involvement with the Guild. Speculators have therefore imagined a great many fantastical abilities, which again he has refused to express any opinion on.'", "Pedestal", 0, 0, [], 0, False])
		level.add_dialog_node("2.0", False, ["'He primarily operates out of the smoking hell-pit that is the city of Chicago, and is often the sole provider of law and order in the dark melee of the nights in that ill-begotten place. His shadow stretches far, however, and it is believed that he has influence over superheroes in other continents, too.'", "Pedestal", 0, 0, [], 0, False])
		level.add_dialog_node("2.0.0", False, ["'Nothing is known of his private life. Very few journalists attempt to speak with him, however, due to the extreme danger present in journeying into the city of Chicago. God rest the souls of those who have tried.'", "Pedestal", 0, 0, [], 0, False])
		level.add_dialog_node("2.0.0.0", True, [[[0, 100], [0, 100], [0, 55], [0, 100], [0, 100]], [], "What an awesome guy.", [0, 0, -3, -1, 0], ["This guy is so cool. I want to be that dark and brooding. I wonder what happened to make him like that?", "Shay de Morta", 0, 0, [], 0, True]])
		level.add_dialog_node("2.0.0.1", True, [[[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]], [], "What a terrible role model.", [0, -1, 0, -2, 2], ["This guy should be ashamed of himself. He's a terrible example for people. He probably smokes and has premarital sex, too. Unbelievable that they would let someone like him into the Guild.", "Shay de Morta", 0, 0, [], 0, True]])
		level.add_dialog_node("2.0.0.2", True, [[[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]], [], "Chicago... What a disaster.", [0, -1, 0, -1, 2], ["Poor guy, having to live in Chicago. I've heard stories about that place. Chills the spine when you think that the kind of people that live there can leave any time they want and live around us.", "Shay de Morta", 0, 0, [], 0, True]])
		
		level.add_dialog_node("3", False, ["'The Saccharine Spirit is an egotist whose powers center around emotion control and incorporeality. She is one of the four founders of the Guild of Heroes, and was a part of the old supergroup 'Justice Friends,' before the tragic events that disbanded the group.'", "Pedestal", 0, 0, [], 0, False])
		level.add_dialog_node("3.0", False, ["'Given that many of her powers work through telecommunications, she has been able to claim a larger range than is normal for egotists of her power; her patrol routes cover the entirety of the Eastwall. She is one of only four superheroes to protect us from the mutant menace beyond.'", "Pedestal", 0, 0, [], 0, False])
		level.add_dialog_node("3.0.0", False, ["'Her origins are fairly well known for an egotist of her renown. A wandering alien ghost, visiting our planet, noticed in her a pure heart and iron will. The spirit, being a protector of the innocent, decided to possess her and and grant her its powers. Thus was the Saccharine Spirit born.'", "Pedestal", 0, 0, [], 0, False])
		level.add_dialog_node("3.0.0.0", True, [[[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]], [], "Her costume, though...", [0, 0, 0, 0, 0], ["She's nice and all. I'm sure she is. She does good work. Heck, she's one of the most famous heroes in the world. I just wish she would put some clothes on. Honestly, is it that hard to buy a jacket and some pants?", "Shay de Morta", 0, 0, [], 0, True]])
		level.add_dialog_node("3.0.0.1", True, [[[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]], [], "We need more like her.", [0, 0, 0, 0, 0], ["Finally, a good female role-model. I can't believe people say that the Guild is sexist. One of their founders is a woman! People are just too sensitive about these things.", "Shay de Morta", 0, 0, [], 0, True]])
		level.add_dialog_node("3.0.0.2", True, [[[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]], [], "Isn't emotion control like being able to roofie people at will?", [0, 0, 0, 0, 0], ["Emotion control, huh? That's kind of intimidating, actually. Talking to someone who could basically be controlling your mind - yeesh. Not sure I actually want to meet her.", "Shay de Morta", 0, 0, [], 0, True]])
		
		level.add_dialog_node("4", False, ["'Silver Rocketeer is a hero of the people. Flying around on his space-age jetpack, he fills out the roster of the founders as one of the most powerful egotists alive. While you wouldn't think it to look at him, villains must beware his jet-powered punch and eagle-like vision.'", "Pedestal", 0, 0, [], 0, False])
		level.add_dialog_node("4.0", False, ["'Making his home in lovely San Fransico, he can be seen daily, protecting the people from such villains as Mr. Mongo, the fiendish Mssrs. Heetler, and Bangbangduck. He is also a founder of the most prolific line of superheroes on record, with almost two dozen direct apprentices.'", "Pedestal", 0, 0, [], 0, False])
		level.add_dialog_node("4.0.0", False, ["'According to the Rocketeer, he received the silver Rocket Pack that jetted him to fame in a tragic Army experiment intended to create a new breed of supersoldiers. Unfortunately, the chemical compound used to irradiate the genetics of the nanomachines used was misapplied, fusing him to the Rocket Pack.'", "Pedestal", 0, 0, [], 0, False])
		level.add_dialog_node("4.0.0.0", False, ["'Fortunately for the rest of us, he has overcome this tragedy and works to ensure that no person need fear the dark while his rocket lights the way.'", "Pedestal", 0, 0, [], 0, False])
		level.add_dialog_node("4.0.0.0.0", True, [[[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]], [], "Oh, man, this guy! I love this guy!", [0, 0, 0, 0, 0], ["I used to love this guy. He was always on the news, cracking wise and stuff. Oh man, it's been years since I read about what he's up to. I wondered what happened to him?", "Shay de Morta", 0, 0, [], 0, True]])
		level.add_dialog_node("4.0.0.0.1", True, [[[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]], [], "This is just too silly.", [0, 0, 0, 0, 0], ["This guy was a little too kiddish for me. Like, I get that some people want to appeal to kids, but seriously, he is just too goofy. God, one of his villains is a guy in a duck costume with a really big gun!", "Shay de Morta", 0, 0, [], 0, True]])
		level.add_dialog_node("4.0.0.0.2", True, [[[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]], [], "Yeah, I could take him.", [0, 0, 0, 0, 0], ["... You know, I think I could take him in a fight. He looks really scrawny. Even his statue looks about ready to pee itself.", "Shay de Morta", 0, 0, [], 0, True]])
		
		level.add_dialog_node("5", False, ["'To eveyone else who keeps the fires of hope and justice burning in their hearts.'", "Pedestal", 0, 0, [], 0, False])
		level.add_dialog_node("5.0", False, ["That's weird. Weren't there five founders to the Guild? This should be the fifth founder's statue.", "Shay de Morta", 0, 0, [], 0, True])
		
		level.add_dialog_node("6", False, ["'To eveyone else who keeps the fires of hope and justice burning in their hearts.'", "Pedestal", 0, 0, [], 0, False])
		level.add_dialog_node("6.0", False, ["Wait, there's something else written here...", "Shay de Morta", 0, 0, [], 0, False])
		level.add_dialog_node("6.0.0", False, ["'The dreams of New Eden will live on in our hearts.'", "Pedestal", 0, 0, [], 0, True])
		
		return level
	elif level_name == "":
		
		pass
		#Initialize level
		#level = Level('NAME.txt', SPR_SHEET, gs)
		#level.adjust_starting_pos(-DISTANCE_TO_CENTER_X, -DISTANCE_TO_CENTER_Y)
		#level.adjust_starting_pos(x, y)
		
		#Create all NPCs
		
		#Create events_dict
		#level.add_events_dict([], [])
		
		#Add Proximity triggers
		
		#Add Event triggers
		
		#Add Dialog nodes
		# level.add_dialog_node("", False, ["", "", 0, , [], , False])
		# level.add_dialog_node("", True, [[[0, 100], [0, 100], [0, 100], [0, 100], [0, 100]], [], "", [0, 0, 0, 0, 0], ["", "Shay de Morta", 0, 0, [], 0, False]])
		
		#return level

def adjx(x):
    return (x)*SPRITE_WIDTH
def adjy(y):
    return (y)*SPRITE_HEIGHT
