import os, sys
from entities import *
import pygame
from pygame.locals import *
from dialog import DialogTree

class Event:
	name = 0
	run = 0

class Conversation(Event):
	#Takes a list of filenames in pictures
	def __init__(self, player, npc, DialogTree, eventsDict):
	#self.lines = [ Line(0, "First line"), Line(0, "Second line")]	
		self.player = player
		self.npc = npc
		self.dialogTree = DialogTree
		self.eventsDict = eventsDict
	

	def do(self, screen, gs):
		box = Talk_Pane("text_box.bmp", 0, (2*(screen.get_size()[1]/3)))

		dialog = self.dialogTree.findDialog(self.npc.conversation_seed)
		id = dialog[0]
		while dialog:
			window = pygame.sprite.Group()
			window.add(box)
			window.draw(screen)
			font = pygame.font.Font(None, 36)
			name = font.render(dialog[1], 1, (255, 255, 255))
			namepos = 15 , 15 + 2*(screen.get_size()[1]/3)
			text = font.render(dialog[2], 1, (255, 255, 255))
			textpos = 15 , 40 + 2*(screen.get_size()[1]/3)
			screen.blit(name, namepos)
			screen.blit(text, textpos)
			pygame.display.flip()
			dialog = self.dialogTree.findNextDialog(id, self.npc.relationship, self.eventsDict)
			if dialog:
				id = id + "." + dialog[0]
			self.wait_input(gs)


	def wait_input(self, gs):
		done = False
		while True:
			for event in pygame.event.get():
				if event.type == QUIT:
					self.quit = True
					return
				if event.type == KEYDOWN:
					gs.kd += 1
					return
				elif event.type == KEYUP:
					gs.kd -= 1
			if done:
				return

 	
class Line:
	text = 0
	#This is an int for which picture to use
	picture = 0
	form = 0

	def __init__(self, picture, text):
		self.picture = picture
		self.text = text

class Talk_Pane(pygame.sprite.Sprite): 
	layer = 2
	interactive = False
	interaction = 0

	def __init__(self, image, x, y, transparent_pixel = True):
		pygame.sprite.Sprite.__init__(self)
		if transparent_pixel:
			self.image, self.rect = load_image(image, -1)
		else:
			colorkey = (255, 0, 255)
			self.image, self.rect = load_image(image, colorkey)
		self.rect.topleft = x, y
	