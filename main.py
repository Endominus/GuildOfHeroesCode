import os, sys
from entities import *
import pygame
from pygame.locals import *

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

def key_pressed():
	x, y = 0, 0
	keysPressed = pygame.key.get_pressed()
	if keysPressed[K_w]:
		y -= 3
	if keysPressed[K_s]:
		y += 3
	if keysPressed[K_a]:
		x -= 3
	if keysPressed[K_d]:
		x += 3
	return x, y

def main():
	pygame.init()
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	pygame.display.set_caption('Guild of Heroes Test')
	pygame.mouse.set_visible(0)
	
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((200, 200, 200))
	
	if pygame.font:
		font = pygame.font.Font(None, 36)
		text = font.render("This is the main Etna window.", 1, (20, 100, 20))
		textpos = text.get_rect(centerx=background.get_width()/2)
		background.blit(text, textpos)
		
	screen.blit(background, (0, 0))
	pygame.display.flip()
	
	frm = Frame()
	frm.bind(-500, 500, -500, 500)
	player = Player_Character('Ghost.bmp', frm)
	rock = Obstacle('Concrete Wall Horizontal.png', 200, 200, frm, False)
	rock2 = Obstacle('Concrete Wall Horizontal.png', 800, 200, frm, False)
	rock3 = Obstacle('Concrete Wall Horizontal.png', 200, 800, frm, False)
	rock4 = Obstacle('Concrete Wall Horizontal.png', 600, 600, frm, False)
	allsprites = pygame.sprite.RenderPlain((player, rock, rock2, rock3, rock4))
	obstacles = pygame.sprite.Group((rock, rock4, rock2, rock3))
	frm.obstruct(player, obstacles)
	clock = pygame.time.Clock()
	

	key_down = 0
	while 1:
		clock.tick(60)
		x, y = 0, 0
		for event in pygame.event.get():
			if event.type == QUIT:
				return
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				return
			elif event.type == KEYDOWN:
				key_down += 1
			elif event.type == KEYUP:
				key_down -= 1
				
		#if key_down:
		#	print "Key down"
		if key_down > 0:
			x, y = key_pressed()
		
		frm.update_keys(x, y)
		frm.run_kinetics()
		
		allsprites.update()
		screen.blit(background, (0, 0))
		allsprites.draw(screen)
		pygame.display.flip()

				
main()
