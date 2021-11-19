import pygame
import numpy as np
import fworldconfig as fwc


class ball:
    def __init__(self):
        self.pt = np.array([100, 300]).astype(float)  # current coordinate
        self.pt0 = np.array([98, 302]).astype(float)  # previous coordinate
        self.rad = 10
        self.nocollisions_yet = True

    def draw(self, screen):
        pygame.draw.circle(screen, [0, 255, 0],
                           (self.pt*fwc.scale).astype(int), int(self.rad*fwc.scale))
