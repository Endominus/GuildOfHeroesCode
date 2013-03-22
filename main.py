import os, sys
from entities import *
import pygame
from pygame.locals import *

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
	screen = pygame.display.set_mode((1600, 900))
	pygame.display.set_caption('Guild of Heroes Test')
	pygame.mouse.set_visible(0)
	
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((200, 200, 200))
	
	if pygame.font:
		font = pygame.font.Font(None, 36)
		text = font.render("This is the main game window.", 1, (20, 100, 20))
		textpos = text.get_rect(centerx=background.get_width()/2)
		background.blit(text, textpos)
		
	screen.blit(background, (0, 0))
	pygame.display.flip()
	
	frm = Frame()
	player = Player_Character('Ghost.bmp')
	rock = Obstacle('Ghost.bmp', 200, 200, frm)
	allsprites = pygame.sprite.RenderPlain((player))
	allsprites2 = pygame.sprite.RenderPlain((rock))
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
		
		player.change_velocity(x, y)
		frm.update_keys(x, y)
		frm.run_kinetics()
		
		allsprites.update()
		allsprites2.update()
		screen.blit(background, (0, 0))
		allsprites.draw(screen)
		allsprites2.draw(screen)
		pygame.display.flip()

				
main()
