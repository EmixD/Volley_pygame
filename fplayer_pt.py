from typing import List
import pygame
import numpy as np
import fworldconfig as fwc


class point:
    pts = []  # type: List[point]

    def __init__(self, id, x, y):
        # static
        self.color = [0, 0, 0]
        self.collision_ball = False
        self.collision_ground = True
        self.allow_print = True
        self.id = id  # just for debugging
        # static hardcoded
        self.mass = 1.0
        self.frict = 0.1  # lateral friction, better be global
        # dynamic
        self.pt = np.array([x, y]).astype(float)  # current coordinate
        self.pt0 = np.array([x, y]).astype(float)  # previous coordinate
        # init
        point.pts.append(self)

    def print(self):
        if(self.allow_print):
            print(f"point id={self.id}: pt={self.pt}. pt0={self.pt0}")

    def draw(self, screen):
        pygame.draw.circle(screen, self.color,
                           (self.pt*fwc.scale).astype(int), int(3*fwc.scale))

    @classmethod
    def get_length(cls,id0,id1):
        return np.linalg.norm(cls.pts[id1].pt-cls.pts[id0].pt)

    @classmethod
    def get_length0(cls,id0,id1):
        return np.linalg.norm(cls.pts[id1].pt0-cls.pts[id0].pt0)
