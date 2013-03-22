import os, sys
import pygame
import math
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

class Obstacle(pygame.sprite.Sprite):
    x_pos = 0
    y_pos = 0
    frame = 0
    #absolute coordinates

    def __init__(self, image, x, y, frm):
	    pygame.sprite.Sprite.__init__(self)
	    self.image, self.rect = load_image(image, -1)
	    screen = pygame.display.get_surface()
	    self.area = screen.get_rect()
	    self.rect.topleft = 100, 100
	    self.x_pos = x
	    self.y_pos = y
	    self.frame = frm
	    self.update()

    def update(self):
	self.rect = (self.x_pos - self.frame.x, self.y_pos - self.frame.y)

    

class Frame:
    #Frame object contains a position representing where the camera is looking
    #on the level. Sprites should take this as an object so they can use its
    #absolute position and their absolute position to determine where to
    #draw themselves on the screen
    
    #top left corner
    x = 0
    y = 0
    #position, pixels
    dxdt = 0
    dydt = 0
    #velocity, pixels/time step
    d2xdt2 = 0
    d2ydt2 = 0
    #accelleration, pixels/time step^2

    #bad physics
    nDamping = 1
    maxSpeed = 8
    accel = 3

    m = -1
    mu_k = -1
    c_d = -1
    f_k = -1
    
    #not implemented
    use_good_physics = False

    def update_keys(self, x, y):
	if x==0:
	    self.d2xdt2 = 0
	else:
	    self.d2xdt2 = math.copysign(self.accel, x)
	
	if y==0:
	    self.d2ydt2 = 0
	else:
	    self.d2ydt2 = math.copysign(self.accel, y)

    def run_kinetics(self):
	self.dxdt += self.d2xdt2
	self.dydt += self.d2ydt2
	
	self.dxdt = min(self.maxSpeed, self.dxdt)
	self.dxdt = max(-self.maxSpeed, self.dxdt)
	self.dydt = min(self.maxSpeed, self.dydt)
	self.dydt = max(-self.maxSpeed, self.dydt)

	if self.dxdt != 0:
	    self.dxdt -= math.copysign(self.nDamping, self.dxdt)
	
	if self.dydt != 0:
	    self.dydt -= math.copysign(self.nDamping, self.dydt)

	self.x += self.dxdt
	self.y += self.dydt















