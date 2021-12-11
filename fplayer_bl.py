import pygame
import numpy as np
import fworldconfig as fwc
import random


class ball:
    def __init__(self,ballindex):
        self.pt = np.array([750-8*ballindex ,50]).astype(float)  # current coordinate
        self.pt0 =self.pt # previous coordinate
        self.rad = 10
        self.nocollisions_yet = True

    def draw(self, screen):
        pygame.draw.circle(screen, [0, 255, 0],
                           (self.pt*fwc.scale).astype(int), int(self.rad*fwc.scale))
