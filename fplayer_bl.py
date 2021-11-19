import pygame
import numpy as np
import fworldconfig as fwc

pt = np.array([100, 100]).astype(float)  # current coordinate
pt0 = np.array([98, 99]).astype(float)  # previous coordinate
rad = 10
nocollisions_yet=True


def draw(screen):
    pygame.draw.circle(screen, [0, 255, 0],
                       (pt*fwc.scale).astype(int), int(rad*fwc.scale))
