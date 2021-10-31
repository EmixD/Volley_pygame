import pygame

class grounds: 
    def __init__(self,y0,x0,x1):
        self.y0=y0
        self.x0=x0
        self.x1=x1
    def draw(self,screen):
        pygame.draw.line(screen, (0, 0, 0),(self.x0,self.y0),(self.x1,self.y0),2)
