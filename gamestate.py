import os, sys
from entities import *
from conversation import *
import pygame
from pygame.locals import*

class Gamestate:
	screen = 0
	background = 0
	frame = 0
	allsprites = 0
	clock = pygame.time.Clock()
	player = 0
	interactables = 0
	NPCs = 0
	quit = False
	interact = False
	held = False

	delay_interact = 0

	#interpreting keys
	x, y = 0, 0
	kd = 0

	def idle(self):
		self.clock.tick(60)
		self._check_input()
		self.frame.run_kinetics()
		self._check_interact()

		self.allsprites.update()

		self.screen.blit(self.background, (0, 0))
		self.allsprites.draw(self.screen)
		pygame.display.flip()


	def __init__(self, screen, background, levelInit):
		self.screen = screen
		self.background = background
		self.frame, self.player, self.interactables, self.allsprites, self.NPCs = levelInit()

	def _check_interact(self):
		if self.interact:
			if self.delay_interact<1:
				self.delay_interact = 15
			collider = pygame.sprite.collide_rect_ratio(1.2)
			collided = pygame.sprite.spritecollide(self.player, self.interactables, False, collider)
			if(len(collided) > 0):
				collided.pop().interaction.do(self.screen, self)
		if self.delay_interact>0:
			self.delay_interact -= 1
			
		for n in self.NPCs:
			#print "screen pos: ", self.frame.x, ":", self.frame.y
			#print "player pos: ", self.player.x, ":", self.player.y
			n.check_vision(self.frame.x + self.player.x, self.frame.y + self.player.y)

	def _check_input(self):
		self.interact = False
		x, y = 0, 0
		for event in pygame.event.get():
			if event.type == QUIT:
				self.quit = True
				return
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				self.quit = True
				return
			elif event.type == KEYDOWN:
				self.kd += 1
			elif event.type ==KEYUP:
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
				self.interact = True
			if keysPressed[K_m]:
				self.frame.lock_frame()
				self.player.toggle_movement()
		self.frame.update_keys(x,y) 
#	if interact
#		self._check_interact()

