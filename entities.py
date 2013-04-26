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
	move_around = False
	passable = False
	x, y = 0, 0
	
	char_OP = 50
	char_CO = 50
	char_EX = 50
	char_AG = 50
	char_NE = 50
	
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
		self.x = 20*32-(SPRITE_WIDTH/2)
		self.y = 15*32-(SPRITE_HEIGHT/2)
		self.rect.topleft = self.x, self.y
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
		if self.move_around:
			newpos = self.rect.move((self.frame.dxdt, self.frame.dydt))
			if not self.area.contains(newpos):
				if self.rect.left < self.area.left or self.rect.right > self.area.right:
					newpos = self.rect.move((-self.frame.dxdt, 0))
					self.frame.dxdt = 0
				if self.rect.top > self.area.top or self.rect.bottom < self.area.bottom:
					newpos = self.rect.move((0, -self.frame.dydt))
					self.frame.dydt = 0
			self.x += self.frame.dxdt
			self.y += self.frame.dydt
			self.rect = newpos
		if self.change_sprite:
			self.image = self.ss.image_at(((self.facing*SPRITE_WIDTH, self.run_state*SPRITE_HEIGHT), (SPRITE_WIDTH, SPRITE_HEIGHT)), (255, 0, 255))
			self.rect = self.image.get_rect()
			self.rect.topleft = self.x, self.y
			self.change_sprite = False
		
	def toggle_movement(self):
		self.move_around = not self.move_around
		
	def change_velocity(self, x, y):
		# if self.vert_velocity > 0:
			# self.vert_velocity = max(0, self.vert_velocity-1)
		# else:
			# self.vert_velocity = min(0, self.vert_velocity+1)
		# if self.hor_velocity > 0:
			# self.hor_velocity = max(0, self.hor_velocity-1)
		# else:
			# self.hor_velocity = min(0, self.hor_velocity+1)
		pass			

class Obstacle(pygame.sprite.Sprite):
	x_pos = 0
	y_pos = 0
	frame = 0
	#absolute coordinates
	
	layer = 2
	interactive = False
	interaction = 0
	interaction_type = 0

	passable = False

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

	lock_screen = False
	
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
		
		if not self.lock_screen:
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

	def lock_frame(self):
		self.lock_screen = not self.lock_screen

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
		
class NPC(Obstacle):
	i = 0
	vision_area_width, vision_area_length = 50, 150
	state = 1
	conversation_seed = -1
	relationship = -1
	facing = 2
	exc = 0
	
	def __init__(self, image, x, y, frm, transparent_pixel = True):
		Obstacle.__init__(self, image, x, y, frm, transparent_pixel)
		self.exc = Obstacle('exclamation.bmp', 500, 500, frm)
		
	def setRelationship(self, x):
		self.relationship = x
		
	def update(self):
		Obstacle.update(self)
		
	def check_vision(self, other_x, other_y):
		self.i += 1
		if self.facing % 4 == 0:
			if self.y_pos - (self.rect.bottom - self.rect.top) / 2 - other_y > 0 and self.y_pos - (self.rect.bottom - self.rect.top) / 2 - other_y < self.vision_area_length:
				if math.fabs(self.x_pos - other_x) < self.vision_area_width and self.state != 0:
					return True
				
		if self.facing % 4 == 1:
			if self.x_pos + (self.rect.right - self.rect.left) / 2 - other_x < 0 and self.x_pos + (self.rect.right - self.rect.left) / 2 - other_x > -1 * self.vision_area_length:
				if math.fabs(self.y_pos - other_y) < 50 and self.state != 0:
					return True	
				
		if self.facing % 4 == 2:
			if self.y_pos + (self.rect.bottom - self.rect.top) / 2 - other_y < 0 and self.y_pos + (self.rect.bottom - self.rect.top) / 2 - other_y > -1 * self.vision_area_length:
				if math.fabs(self.x_pos - other_x) < self.vision_area_width and self.state != 0:
					return True
				
		if self.facing % 4 == 3:
			if self.x_pos - (self.rect.right - self.rect.left) / 2 - other_x > 0 and self.x_pos - (self.rect.right - self.rect.left) / 2 - other_x < self.vision_area_length:
				if math.fabs(self.y_pos - other_y) < 50 and self.state != 0:
					return True	
				
		return False
		
	def set_seed(self, x):
		self.conversation_seed = x
		
	def change_facing(self, direction):
		self.image = pygame.transform.rotate(self.image, (self.facing % 4 - direction % 4) * 90)
		self.rect = self.image.get_rect()
		self.facing = direction
		
	def set_state(self, new_state, frm):
		self.state = newstate
		
	def take_action(self, action, screen, x, y):
		self.exc.x_pos = self.x_pos + 5
		self.exc.y_pos = self.y_pos - 40
		return self.exc

class Event(object):

#Type Codes:
# 0 = Start Conversation
	# vals = [gs, npc]
# 1 = Change Level
	# vals = [gs, levelname]
# 2 = Set/Reset Trigger
	# vals = [[keys], [values]]
	def __init__(self, trigger, type, val):
		self.triggers = trigger
		self.type = type
		self.vals = val
		
	def do(events):
		#for i in range(len(self.triggers)
	
		if self.trigger in events and events[self.trigger]:
			if self.type == 0:
				events[self.trigger] = False
				val[0].converse = True
				val[0].conversation_npc = val[1]
			elif self.type == 1:
				events[self.trigger] = False
				val[0].change_level = True
				val[0].level_to_change = val[1]
			elif self.type == 2:
				events[self.trigger] = False
				for i in range(len(self.vals[0])):
					if self.vals[0][i] in events:
						events[self.vals[0][i]] = self.vals[1][i]
			
