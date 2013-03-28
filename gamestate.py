import os, sys
from entities import &
import pygame
from pygame.locals import*
import prolouge_outside

def gamestate:
    screen
    background
    frame
    allsprites
    clock = pygame.time.Clock()
    player
    interactables
    quit = False
    
    #interpreting keys
    x, y = 0
    kd = 0
    
    def idle():
    clock.tick(60)
    self.check_input
    self.frame.run_kinetics()
    
    self.allsprites.update()
    self.screen.blit(self.background, (0, 0))
    self.allsprites.draw(self.screen)
    pygame.display.flip()

    def check_interact(self):
    collider = pygame.sprite.collide_rect_ratio(1.2)
    collided = pygame.sprite.collide(self.player, self.interactables, False, collider)
        
    
    def _check_input():
    interact = False
    for event in pygame.event.get():
        if event.type == QUIT:
        quit = True
        return
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
        quit = True
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
        interact = True
    
    self.frame.update_keys(x, y)
    if interact
        self.player.check_interact
