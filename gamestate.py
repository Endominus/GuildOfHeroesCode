import os, sys
from entities import *
from conversation import *
import pygame
from pygame.locals import*

class Gamestate:
    screen = 0
    background = 0
    frame = 0
    allsprites = 0
    clock = pygame.time.Clock()
    player = 0
    interactables = 0
    quit = False
    interact = False
    
    #interpreting keys
    x, y = 0, 0
    kd = 0
    
    def idle(self):
	self.clock.tick(60)
        self._check_input()
        self.frame.run_kinetics()
        self._check_interact()

        self.allsprites.update()

        self.screen.blit(self.background, (0, 0))
        self.allsprites.draw(self.screen)
        pygame.display.flip()

    def __init__(self, screen, background, levelInit):
        self.screen = screen
        self.background = background
        self.frame, self.player, self.interactables, self.allsprites = levelInit() 

    def _check_interact(self):
	if self.interact:
	    collider = pygame.sprite.collide_rect_ratio(1.2)
	    collided = pygame.sprite.spritecollide(self.player, self.interactables, False, collider)
	    if(len(collided) > 0):
		collided.pop().interaction.do()

    def _check_input(self):
	self.interact = False
        x, y = 0, 0
        for event in pygame.event.get():
            if event.type == QUIT:
                self.quit = True
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                self.quit = True
                return
            elif event.type == KEYDOWN:
                self.kd += 1
            elif event.type ==KEYUP:
                self.kd -= 1 
        keysPressed = pygame.key.get_pressed()
    
        if self.kd > 0:
            if keysPressed[K_w]:
                y -= 1
            if keysPressed[K_s]:
                y += 1
            if keysPressed[K_a]:
                x -= 1
            if keysPressed[K_d]:
                x += 1
            if keysPressed[K_f]:
                self.interact = True
        self.frame.update_keys(x,y) 
#    if interact
#        self._check_interact()

