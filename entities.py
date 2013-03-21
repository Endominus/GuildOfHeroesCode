import os, sys
import pygame
from pygame.locals import *

MAX_SPEED = 8

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

class Player_Character(pygame.sprite.Sprite):
	"""Main character, Ghost. This controls her image on the screen."""
	vert_velocity = 0
	hor_velocity = 0
	def __init__(self, image):
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image(image, -1)
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.rect.topleft = 100, 100
		self.vert_velocity = 0
		self.hor_velocity = 0
	
	def _degradeSpeed(self):
		if self.vert_velocity > 0:
			self.vert_velocity = max(0, self.vert_velocity-1)
		else:
			self.vert_velocity = min(0, self.vert_velocity+1)
		if self.hor_velocity > 0:
			self.hor_velocity = max(0, self.hor_velocity-1)
		else:
			self.hor_velocity = min(0, self.hor_velocity+1)
	
	def update(self):
		newpos = self.rect.move((self.hor_velocity, self.vert_velocity))
		if not self.area.contains(newpos):
			if self.rect.left < self.area.left or self.rect.right > self.area.right:
				newpos = self.rect.move((-self.hor_velocity, 0))
				self.hor_velocity = 0
			if self.rect.top > self.area.top or self.rect.bottom < self.area.bottom:
				newpos = self.rect.move((0, -self.vert_velocity))
				self.vert_velocity = 0
		self.rect = newpos
		
	def change_velocity(self, x, y):
		if y < 0:
			self.vert_velocity = max(-MAX_SPEED, self.vert_velocity+y)
		elif y > 0:
			self.vert_velocity = min(MAX_SPEED, self.vert_velocity+y)
		if x > 0:
			self.hor_velocity = min(MAX_SPEED, self.hor_velocity + x)
		elif x < 0:
			self.hor_velocity = max(-MAX_SPEED, self.hor_velocity + x)
		self._degradeSpeed()
