import pygame
import fworldconfig as fwc

class grounds: 
    def __init__(self,y0,x0,x1):
        self.y0=y0
        self.x0=x0
        self.x1=x1
    def draw(self,screen):
        pygame.draw.line(screen, (0, 0, 0),(self.x0*fwc.scale,self.y0*fwc.scale),(self.x1*fwc.scale,self.y0*fwc.scale),2*fwc.scale)
