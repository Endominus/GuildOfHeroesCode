import os, sys
from entities import *
from gamestate import *
import pygame
from pygame.locals import *
import prologue_outside
import prologue_hall
import pathfinding
import pygame.mixer

SCREEN_WIDTH = 16*SPRITE_WIDTH
SCREEN_HEIGHT = 10*SPRITE_HEIGHT

def key_pressed():
	x, y = 0, 0
	keysPressed = pygame.key.get_pressed()
	if keysPressed[K_w]:
		y -= 2
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
	background.fill((20, 20, 20))
	
	if pygame.font:
		font = pygame.font.Font(None, 36)
		text = font.render(" ", 1, (20, 100, 20))
		textpos = text.get_rect(centerx=background.get_width()/2)
		background.blit(text, textpos)
		
	screen.blit(background, (0, 0))
	pygame.display.flip()

	gs = Gamestate(screen, background, "prologue_outside")
	
	while (not gs.quit):
		gs.idle()
	
main()
