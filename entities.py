import os, sys
import pygame
import math
from pygame.locals import *

MAX_SPEED = 8
SPRITE_WIDTH = 14
SPRITE_HEIGHT = 20

class spritesheet(object):
	def __init__(self, filename):
		try:
			self.sheet = pygame.image.load(filename).convert()
		except pygame.error, message:
			print 'Unable to load spritesheet image:', filename
			raise SystemExit, message
	# Load a specific image from a specific rectangle
	def image_at(self, rectangle, colorkey = None):
		"Loads image from x,y,x+offset,y+offset"
		rect = pygame.Rect(rectangle)
		image = pygame.Surface(rect.size).convert()
		image.blit(self.sheet, (0, 0), rect)
		if colorkey is not None:
			if colorkey is -1:
				colorkey = image.get_at((0,0))
			image.set_colorkey(colorkey, pygame.RLEACCEL)
		return image
	# Load a whole bunch of images and return them as a list
	def images_at(self, rects, colorkey = None):
		"Loads multiple images, supply a list of coordinates" 
		return [self.image_at(rect, colorkey) for rect in rects]
	# Load a whole strip of images
	def load_strip(self, rect, image_count, colorkey = None):
		"Loads a strip of images and returns them as a list"
		tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
				for x in range(image_count)]
		return self.images_at(tups, colorkey)

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
	frame = 0
	layer = 3
	facing = 0
	run_state = 0
	state_counter = 0
	ss = 0
	change_sprite = False
	def __init__(self, image, frm):
		pygame.sprite.Sprite.__init__(self)
		#self.image, self.rect = load_image(image, -1)
		self.facing = 0
		self.run_state = 0
		self.state_counter = 0
		image_name = os.path.join('data', image)
		self.ss = spritesheet(image_name)
		self.image = self.ss.image_at(((self.facing*SPRITE_WIDTH, self.run_state*SPRITE_HEIGHT), (SPRITE_WIDTH, SPRITE_HEIGHT)), (255, 0, 255))
		self.rect = self.image.get_rect()
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.rect.topleft = 20*32-16, 15*32-16
		self.frame = frm
		
#	def _degradeSpeed(self):
#		if y < 0:
#			self.vert_velocity = max(-MAX_SPEED, self.vert_velocity+y)
#		elif y > 0:
#			self.vert_velocity = min(MAX_SPEED, self.vert_velocity+y)
#		if x > 0:
#			self.hor_velocity = min(MAX_SPEED, self.hor_velocity + x)
#		elif x < 0:
#			self.hor_velocity = max(-MAX_SPEED, self.hor_velocity + x)
#		self._degradeSpeed()

	def change_facing(self, direction):
		if abs(direction) > 3:
			print "That's a lot of facing! I've got an error here!"
		else:
			self.facing = direction
			self.change_sprite = True
			
	def cycle_run_state(self, continue_motion):
		if continue_motion:
			self.state_counter += 1
			if self.run_state == 0:
				self.run_state = 1
		else:
			self.state_counter = 0
			self.run_state = 0
		if self.state_counter > 10:
			self.state_counter = 0
			self.run_state = (self.run_state + 1) % 6
			self.change_sprite = True
			
	
	def update(self):
		# newpos = self.rect.move((self.hor_velocity, self.vert_velocity))
		# if not self.area.contains(newpos):
			# if self.rect.left < self.area.left or self.rect.right > self.area.right:
				# newpos = self.rect.move((-self.hor_velocity, 0))
				# self.hor_velocity = 0
			# if self.rect.top > self.area.top or self.rect.bottom < self.area.bottom:
				# newpos = self.rect.move((0, -self.vert_velocity))
				# self.vert_velocity = 0
		# self.rect = newpos
		if abs(self.frame.dxdt) > abs(self.frame.dydt):
			if self.frame.dxdt > 0:
				self.change_facing(3)
			else:
				self.change_facing(1)
		elif abs(self.frame.dxdt) < abs(self.frame.dydt):
			if self.frame.dydt > 0:
				self.change_facing(0)
			else:
				self.change_facing(2)
		self.cycle_run_state(self.frame.dxdt != 0 or self.frame.dydt != 0)
		if self.change_sprite:
			self.image = self.ss.image_at(((self.facing*SPRITE_WIDTH, self.run_state*SPRITE_HEIGHT), (SPRITE_WIDTH, SPRITE_HEIGHT)), (255, 0, 255))
			self.rect = self.image.get_rect()
			self.rect.topleft = 20*32-16, 15*32-16
			self.change_sprite = False
		
	# def change_velocity(self, x, y):
		# if self.vert_velocity > 0:
			# self.vert_velocity = max(0, self.vert_velocity-1)
		# else:
			# self.vert_velocity = min(0, self.vert_velocity+1)
		# if self.hor_velocity > 0:
			# self.hor_velocity = max(0, self.hor_velocity-1)
		# else:
			# self.hor_velocity = min(0, self.hor_velocity+1)
			

class Obstacle(pygame.sprite.Sprite):
	x_pos = 0
	y_pos = 0
	frame = 0
	#absolute coordinates
	
	layer = 2
	interactive = False
	interaction = 0

	def __init__(self, image, x, y, frm, transparent_pixel = True):
		pygame.sprite.Sprite.__init__(self)
		if transparent_pixel:
			self.image, self.rect = load_image(image, -1)
		else:
			colorkey = (255, 0, 255)
			self.image, self.rect = load_image(image, colorkey)
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.rect.topleft = 100, 100
		self.x_pos = x
		self.y_pos = y
		self.frame = frm
		self.update()


	def update(self):
		self.rect.topleft = self.x_pos - self.frame.x, self.y_pos - self.frame.y

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

	m = 100.0
	mu_k = 0.3
	c_d = 0.1
	f_k = 10.0

	#not implemented
	use_good_physics = False

	#boundary to navigable area
	x_min = 0
	x_max = 0
	y_min = 0
	y_max = 0
	bound = False

	#obsctacles
	obstacles = []
	obstructed = False
	player = 0

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
		if self.use_good_physics==False:
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
		else:
			#accelleration
			self.dxdt += (self.d2xdt2*f_k)/m
			self.dydt += (self.d2ydt2*f_k)/m
		
		#print "dx ", self.dxdt
		#print "dy ", self.dydt
			
		self.fixcollision()
		self.x += self.dxdt
		self.y += self.dydt

		
		if(self.bound):
			self.x = max(self.x, self.x_min)
			self.x = min(self.x, self.x_max)
			self.y = max(self.y, self.y_min)
			self.y = min(self.y, self.y_max)
	
	def bind(self, x1, x2, y1, y2):
		self.x_min = x1
		self.x_max = x2
		self.y_min = y1
		self.y_max = y2
		self.bound = True

	def obstruct(self, player, group):
		
		self.obstacles = group
		self.player = player
		self.obstructed = True



	def fixcollision(self):
		if(self.obstructed):
			collided = pygame.sprite.spritecollide(self.player, self.obstacles, False)
			#TODO: put player outside of the object
			if(len(collided) > 0):
				return
			
			#check collision in x
			self.player.rect.move_ip(self.dxdt, 0)  
			collided = pygame.sprite.spritecollide(self.player, self.obstacles, False)
			self.player.rect.move_ip(-self.dxdt, 0)
			if(len(collided) > 0):
				self.dxdt = 0

			#check collision in y
			self.player.rect.move_ip(0, self.dydt)  
			collided = pygame.sprite.spritecollide(self.player, self.obstacles, False)
			self.player.rect.move_ip(0, -self.dydt)
			if(len(collided) > 0):
				self.dydt = 0

			#check collision in diagonal
			self.player.rect.move_ip(0, self.dxdt)  
			self.player.rect.move_ip(0, self.dydt)  
			collided = pygame.sprite.spritecollide(self.player, self.obstacles, False)
			self.player.rect.move_ip(0, -self.dxdt)
			self.player.rect.move_ip(0, -self.dydt)
			if(len(collided) > 0):
				self.dxdt = 0
				self.dydt = 0


class Event:
    name = 0
    run = 0

class Simple_Conversation(Event):
    lines = 0
    pictures = 0
    
    #Takes a list of filenames in pictures
    def __init__(self, statements, pictures, form):
	#self.lines = [ Line(0, "First line"), Line(0, "Second line")]	
	self.lines = []
	for s in statements:
	    self.lines.append(Line(0, s))
	

    def do(self, screen, gs):
	box = Talk_Pane("text_box.bmp", 0, (2*(screen.get_size()[1]/3)))

	for line in self.lines:
	    window = pygame.sprite.Group()
	    window.add(box)
	    window.draw(screen)
	    font = pygame.font.Font(None, 36)
	    text = font.render(line.text, 1, (255, 255, 255))
	    textpos = 15 , 15 + 2*(screen.get_size()[1]/3)
	    screen.blit(text, textpos)
	    pygame.display.flip()
	    self.wait_input(gs)


    def wait_input(self, gs):
	while True:
	    done = False
	    for event in pygame.event.get():
		if event.type == KEYDOWN:
		    gs.kd += 1
		    done = True
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



