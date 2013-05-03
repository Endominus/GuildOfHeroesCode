import os, sys
from entities import *
import pygame
from pygame.locals import *
from dialog import DialogTree

class Conversation(object):
	#Takes a list of filenames in pictures
	def __init__(self, player, npc, DialogTree, eventsDict):
	#self.lines = [ Line(0, "First line"), Line(0, "Second line")]	
		self.player = player
		self.npc = npc
		self.dialogTree = DialogTree
		self.eventsDict = eventsDict
		self.choice = False
		self.num_choices = 0
		self.kd = 0
		self.selected_choice = 0
		self.lock = True
	

	def do(self, screen, gs):
		box = Talk_Pane("text_box.bmp", 0, (2*(screen.get_size()[1]/3)))

		dialog = self.dialogTree.findDialog(self.npc.conversation_seed)
		id = dialog[0]
		characteristics = [self.player.char_OP, self.player.char_CO, self.player.char_EX, self.player.char_AG, self.player.char_NE]
		while dialog:
			window = pygame.sprite.Group()
			window.add(box)
			window.draw(screen)
			font = pygame.font.Font(None, 36)
			if type(dialog[0]) == list:
				self.choice = True
				self.num_choices = 0
				self.selected_choice = 0
				for node in dialog:
					text = font.render(node[1], 1, (255, 255, 255))
					textpos = 45 , 40 + 2*(screen.get_size()[1]/3) + 25*self.num_choices
					screen.blit(text, textpos)
					self.num_choices += 1
				pointer = font.render("->", 1, (255, 255, 255))
				pointerpos = 15 , 40 + 2*(screen.get_size()[1]/3) + 25*self.selected_choice
				screen.blit(pointer, pointerpos)
				pygame.display.flip()
				self.wait_input(gs, screen)
				id = id + "." + dialog[self.selected_choice][0]
				print id
				dialog = self.dialogTree.findDialog(id)
			else:
				name = font.render(dialog[1], 1, (255, 255, 255))
				namepos = 15 , 15 + 2*(screen.get_size()[1]/3)
				text = font.render(dialog[2], 1, (255, 255, 255))
				textpos = 15 , 40 + 2*(screen.get_size()[1]/3)
				screen.blit(name, namepos)
				screen.blit(text, textpos)
				pygame.display.flip()
				dialog = self.dialogTree.findNextDialog(id, self.npc.relationship, self.eventsDict, characteristics)
				if dialog and type(dialog[0]) != list:
					id = id + "." + dialog[0]
				self.wait_input(gs, screen)


	def wait_input(self, gs, screen):
		done = False
		while True:
			for event in pygame.event.get():
				if event.type == QUIT:
					gs.quit = True
					return
				elif event.type == KEYDOWN and event.key == K_ESCAPE:
					gs.quit = True
					return
				elif event.type == KEYDOWN:
					gs.kd += 1
					#self.kd += 1
				elif event.type == KEYUP:
					gs.kd -= 1
					if gs.kd < 0:
						gs.kd = 0
					self.lock = False
					#self.kd -= 1
			keysPressed = pygame.key.get_pressed()
					
			if gs.kd > 0 and not self.lock:
				if self.choice:
					window = pygame.sprite.Group()
					window.draw(screen)
					font = pygame.font.Font(None, 36)
					if keysPressed[K_w]:
						pointer = font.render("->", 1, (0, 112, 159))
						pointerpos = 15 , 40 + 2*(screen.get_size()[1]/3) + 25*self.selected_choice
						screen.blit(pointer, pointerpos)
						self.selected_choice -= 1
						if self.selected_choice < 0:
							self.selected_choice += self.num_choices
						gs.kd = 0
					if keysPressed[K_s]:
						pointer = font.render("->", 1, (0, 112, 159))
						pointerpos = 15 , 40 + 2*(screen.get_size()[1]/3) + 25*self.selected_choice
						screen.blit(pointer, pointerpos)
						self.selected_choice = (self.selected_choice + 1) % self.num_choices
						gs.kd = 0
					pointer = font.render("->", 1, (255, 255, 255))
					pointerpos = 15 , 40 + 2*(screen.get_size()[1]/3) + 25*self.selected_choice
					screen.blit(pointer, pointerpos)
					pygame.display.flip()
				if keysPressed[K_SPACE]:
					self.lock = True
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
	