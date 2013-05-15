import os, sys
from entities import *
from conversation import *
import pygame
from pygame.locals import*
from level import *

class Gamestate:
	screen = 0
	background = 0
	frame = 0
	allsprites = 0
	clock = pygame.time.Clock()
	player = 0
	NPCs = 0
	quit = False
	interact = False
	held = False
	dialogTree = False
	eventsDict = {'action_button':False}
	level = 0

	levelWidth = 40*SPRITE_WIDTH#16*SPRITE_WIDTH
	levelHeight = 12*SPRITE_WIDTH#10*SPRITE_HEIGHT
	#Damnit, ahmed, this is the size of the level- not of the screen.
	#shouldn't be constant

	delay_interact = 0

	#interpreting keys
	x, y = 0, 0
	kd = 0
	
	converse = False
	conversation_seed = 0
	conversation_npc = 0
	
	change_level = False
	level_to_change = 0

	def idle(self):
		self.clock.tick(60)
		self._check_input()
		self.frame.run_kinetics()
		for trigger in self.proximity_triggers:
			trigger.do(self.player, self.eventsDict)
		for trigger in self.event_triggers:
			trigger.do(self.eventsDict)
		self._check_interact()

		self.allsprites.update()

		self.screen.blit(self.background, (0, 0))
		self.allsprites.draw(self.screen)
		pygame.display.flip()

	def new_level(self, level_name):
		#self.frame, self.player, self.interactables, self.allsprites, self.NPCs, self.dialogTree = level.initialize_level()
		level = load_level(level_name, self)
		self.frame = level.frm
		self.player = level.player
		self.event_triggers = level.event_triggers
		for trigger in self.event_triggers:
			trigger.set_gs(self)
		self.proximity_triggers = level.proximity_triggers
		self.allsprites = level.allsprites
		self.NPCs = level.NPCs
		self.dialogueTree = level.dT
		for event in level.events.keys():
			self.eventsDict[event] = level.events[event]
		self.level = level

	def __init__(self, screen, background, levelInit):
		self.screen = screen
		self.background = background
		self.new_level(levelInit)
		
	def _check_interact(self):
		if self.interact:
			if self.delay_interact<1:
				self.delay_interact = 20
				if self.converse:
					convo = Conversation(self.player, self.conversation_seed, self.conversation_npc, self.level.dT, self.eventsDict)
					convo.do(self.screen, self)
				elif self.change_level:
					self.new_level(self.level_to_change)
		
		self.converse = False
		self.change_level = False

		if self.delay_interact>0:
			self.delay_interact -= 1
			
		# for n in self.NPCs:
##			print "screen pos: ", self.frame.x, ":", self.frame.y
##			print "player pos: ", self.player.x, ":", self.player.y
			# if n.check_vision(self.frame.x + self.player.x, self.frame.y + self.player.y):
				# self.allsprites.add(n.take_action(1, self.frame, self.frame.x + self.player.x, self.frame.y + self.player.y))
##				if n.guard_behavior:
##				   n.chase(self.player)
			# else:
				# self.allsprites.remove(n.take_action(1, self.frame, self.frame.x + self.player.x, self.frame.y + self.player.y))
				

	def _check_input(self):
		self.interact = True
		x, y = 0, 0
		for event in pygame.event.get():
			if event.type == QUIT:
				self.quit = True
				return
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				self.quit = True
				return
			elif event.type == KEYDOWN and event.key == K_m:
				self.kd += 1
				print "Openness:", self.player.char_OP
				print "Conscientiousness:", self.player.char_CO
				print "Extroversion:", self.player.char_EX
				print "Agreeableness:", self.player.char_AG
				print "Neuroticism:", self.player.char_NE 
			elif event.type == KEYDOWN:
				self.kd += 1
			elif event.type == KEYUP:
				self.kd -= 1 
		keysPressed = pygame.key.get_pressed()
	
		if self.kd > 0:
			if keysPressed[K_w]:
				y -= 1
			if keysPressed[K_s]:
				y += 1
			if keysPressed[K_a]:
				x -= 1
			if keysPressed[K_d]:
				x += 1
			if keysPressed[K_SPACE]:
				#self.interact = True
				self.eventsDict['action_button'] = True
			else:
				#self.interact = False
				self.eventsDict['action_button'] = False
			#if keysPressed[K_m]:
				#self.frame.lock_frame()
				#self.player.toggle_movement()
		else:
			self.eventsDict['action_button'] = False
			
		self.frame.update_keys(x,y) 
#	if interact
#		self._check_interact()

