import os, sys
import pygame
import math
from pygame.locals import *
import pathfinding
from pathfinding import *

MAX_SPEED = 8
SPRITE_WIDTH = 64
SPRITE_HEIGHT = 64

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

def load_image(name, colorkey=None,):
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

	#Player's absolute position, used for pathing
	x_pos, y_pos = 0, 0
	
	char_OP = 50
	char_CO = 50
	char_EX = 50
	char_AG = 50
	char_NE = 50
	
	current_sprite_width = 28
	current_sprite_height = 40
	
	def __init__(self, image, frm):
		pygame.sprite.Sprite.__init__(self)
		#self.image, self.rect = load_image(image, -1)
		self.facing = 0
		self.run_state = 0
		self.state_counter = 0
		image_name = os.path.join('data', image)
		self.ss = spritesheet(image_name)
		self.image = self.ss.image_at(((self.facing*self.current_sprite_width, self.run_state*self.current_sprite_height), (self.current_sprite_width, self.current_sprite_height)), (255, 0, 255))
		#self.image = pygame.transform.scale2x(self.image)
		self.rect = self.image.get_rect()
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.x = 8*SPRITE_WIDTH-(self.current_sprite_width/2)
		self.y = 5*SPRITE_HEIGHT-(self.current_sprite_height/2)
		self.rect.topleft = self.x, self.y
		self.frame = frm
		self.x_pos = self.x
		self.y_pos = self.y

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
			self.change_sprite = True
		if self.state_counter > 10:
			self.state_counter = 0
			self.run_state = (self.run_state % 4) + 1
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
			self.image = self.ss.image_at(((self.facing*self.current_sprite_width, self.run_state*self.current_sprite_height), (self.current_sprite_width, self.current_sprite_height)), (255, 0, 255))
			self.rect = self.image.get_rect()
			self.rect.topleft = self.x, self.y
			#self.image = pygame.transform.scale2x(self.image)
			self.change_sprite = False
		self.x_pos += self.frame.dxdt
		self.y_pos += self.frame.dydt

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
		
	def change_stats(self, OP, CO, EX, AG, NE):
		if OP > -1:
			self.char_OP = (self.char_OP + OP)/2
			self.char_OP = max(0, self.char_OP)
			self.char_OP = min(100, self.char_OP)
		if CO > -1:
			self.char_CO = (self.char_CO + CO)/2
			self.char_CO = max(0, self.char_CO)
			self.char_CO = min(100, self.char_CO)
		if EX > -1:
			self.char_EX = (self.char_EX + EX)/2
			self.char_EX = max(0, self.char_EX)
			self.char_EX = min(100, self.char_EX)
		if AG > -1:
			self.char_AG = (self.char_AG + AG)/2
			self.char_AG = max(0, self.char_AG)
			self.char_AG = min(100, self.char_AG)
		if NE > -1:
			self.char_NE = (self.char_NE + NE)/2
			self.char_NE = max(0, self.char_NE)
			self.char_NE = min(100, self.char_NE)

class Obstacle(pygame.sprite.Sprite):
	x_pos = 0
	y_pos = 0
	frame = 0
	#absolute coordinates
	
	gs = 0
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
	relationship = -1
	facing = 2
	exc = 0
	id = 0
	speed = 5
	movement_target = 0
	movement_target_node = 0
	movement_path = 0
	movement_path_life = 0
	movement_path_init_life = 15

	guard_behavior = False
	
	def __init__(self, image, x, y, frm, id, transparent_pixel = True):
		Obstacle.__init__(self, image, x, y, frm, transparent_pixel)
		self.exc = Obstacle('exclamation.bmp', 500, 500, frm)
		self.id = id
		
	def setRelationship(self, x):
		self.relationship = x
		
	def update(self):
		if(self.movement_target != 0):
		    self.movement_path
		    #generate path
		    if(self.movement_path_life == 0):
			self.movement_path = find_path(self.gs, self, self.movement_target)
			self.movement_path_life = self.movement_path_init_life
			self.movement_target_node = (self.y_pos, self.x_pos)

		    #check node
		    if( (self.x_pos == self.movement_target_node[1]) and (self.y_pos == self.movement_target_node[0])):
			if(len(self.movement_path) > 0):
			    self.movement_target_node = self.movement_path.pop()
			else:
			    self.movement_target_node = (self.y_pos, self.x_pos)

		    if(self.x_pos > self.movement_target_node[1]):
			dx = -self.speed
		    elif(self.x_pos < self.movement_target_node[1]):
			dx = self.speed
		    else:
			dx = 0

		    if(self.y_pos > self.movement_target_node[0]):
			dy = -self.speed
		    elif(self.y_pos < self.movement_target_node[0]):
			dy = self.speed
		    else:
			dy = 0

		    if((dx != 0) and (dy != 0)):
			dx = int(dx/1.414)
			dy = int(dy/1.414)

		    self.x_pos += dx
		    self.y_pos += dy
		    self.movement_path_life -= 1
		
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

	def chase(self, target):
		self.movement_target = target
		return

class AnimatedNPC(NPC):
	i = 0
	vision_area_width, vision_area_length = 50, 150
	state = 1
	relationship = -1
	animation = 0
	animation_timer = 0
	idle_animation_timer = 60
	exc = 0
	id = 0
	speed = 5
	movement_target = 0
	movement_target_node = 0
	movement_path = 0
	movement_path_life = 0
	movement_path_init_life = 15
	change_sprite = False
	
	def __init__(self, image, loc, sizes, frm, id, frames):
		NPC.__init__(self, image, loc[0], loc[1], frm, id)
		pygame.sprite.Sprite.__init__(self)
		self.sprite_width = sizes[0]
		self.sprite_height = sizes[1]
		self.run_state = 0
		self.facing = 0
		
		image_name = os.path.join('data', image)
		self.ss = spritesheet(image_name)
		self.image = self.ss.image_at(((self.facing*self.sprite_width, self.run_state*self.sprite_height), (self.sprite_width, self.sprite_height)), (255, 0, 255))
		self.image = pygame.transform.scale2x(self.image)
		self.rect = self.image.get_rect()
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.rect.topleft = loc[0], loc[1]
		self.x = loc[0]
		self.y = loc[1]
		self.x_pos = loc[0]
		self.y_pos = loc[1]
		self.frame = frm
		self.walk_frames = frames[0]
		self.idle_frames = frames[1]
		self.update()
		
	def cycle_run_state(self):
		if self.animation > 0:
			self.animation_timer -= 1
			self.idle_animation_timer = 240
		else:
			self.run_state = 0
			self.idle_animation_timer -= 1
			if self.idle_animation_timer == 0:
				self.run_state = self.walk_frames
				self.animation = 2
			self.change_sprite = False
		if self.animation_timer == 0:
			if self.animation == 1:
				self.animation_timer = 15
				self.run_state = (self.run_state % self.walk_frames) + 1
				self.change_sprite = True
			elif self.animation == 2:
				self.animation_timer = 30
				self.run_state += 1
				if self.run_state > self.idle_frames + self.walk_frames:
					self.animation = 0
					self.run_state = 0
				self.change_sprite = True
				
	def update(self):
		self.cycle_run_state()
		if self.change_sprite:
			self.image = self.ss.image_at(((self.facing*self.sprite_width, self.run_state*self.sprite_height), (self.sprite_width, self.sprite_height)), (255, 0, 255))
			self.rect = self.image.get_rect()
			self.rect.topleft = self.x, self.y
			self.image = pygame.transform.scale2x(self.image)
			self.change_sprite = False
		
		Obstacle.update(self)
		
class EventTrigger(object):

	gs = 0

#Type Codes:
# 0 = Start Conversation
	# vals = [seed, npc]
# 1 = Change Level
	# vals = levelname
# 2 = Set/Reset Trigger
	# vals = [[keys], [values]]
	def __init__(self, trigger, type, val):
		self.triggers = trigger
		self.type = type
		self.vals = val
		
	def do(self, events):
		for i in range(len(self.triggers)):
			if self.triggers[i] not in events or not events[self.triggers[i]]:
				return
		if self.type == 0:
			#events[self.trigger] = False
			#print events
			self.gs.converse = True
			self.gs.conversation_seed = self.vals[0]
			self.gs.conversation_npc = self.vals[1]
		elif self.type == 1:
			#events[self.trigger] = False
			self.gs.change_level = True
			self.gs.level_to_change = self.vals
		elif self.type == 2:
			#events[self.trigger] = False
			for i in range(len(self.vals[0])):
				if self.vals[0][i] in events:
					events[self.vals[0][i]] = self.vals[1][i]
							
	def set_gs(self, gs):
		self.gs = gs
					
class ProximityTrigger(pygame.sprite.Sprite):
	anchor = 0
	link_loc = 0
	
	#key value format: [[key, value], [key2, value2]]
	def __init__(self, location, width, height, triggers, keys, unstable):
		pygame.sprite.Sprite.__init__(self)
		screen = pygame.display.get_surface()
		self.area = screen.get_rect()
		self.rect = Rect(location[0], location[1], width, height)
		self.triggers = triggers
		self.key_values = keys
		self.stability = unstable
		
	def link_object(self, npc):
		self.anchor = npc
		#self.link_loc = [npc.x_pos, npc.y_pos]
		self.link_loc = [npc.rect.x, npc.rect.y]
		self.rect = npc.rect.copy()
		#self.rect.x = npc.x_pos
		#self.rect.y = npc.y_pos
		self.rect = self.rect.inflate(20, 20)
		
	def do(self, player, events):
		
		if self.anchor:
			self.rect.move_ip(self.anchor.rect.x - self.link_loc[0], self.anchor.rect.y - self.link_loc[1])
			self.link_loc[0] = self.anchor.rect.x
			self.link_loc[1] = self.anchor.rect.y
			#print "Player Pos:", player.x, player.y
			#print "Trigger Pos:", self.rect.x, self.rect.y
			playerRect = player.rect
		else:
			playerRect = Rect(player.x_pos, player.y_pos, player.current_sprite_width, player.current_sprite_height)
		if self.rect.colliderect(playerRect):
			#print "Colliding"
			for key in self.triggers:
				if key not in events or (not events[key]):
					return
			for key_value in self.key_values:
				events[key_value[0]] = key_value[1]
		elif self.stability:
			
			for key_value in self.key_values:
				events[key_value[0]] = not key_value[1]
