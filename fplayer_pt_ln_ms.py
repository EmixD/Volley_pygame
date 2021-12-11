from typing import List
import pygame
import numpy as np
import fworldconfig as fwc


class point:
    def __init__(self, id, x, y):  # id is just for debugging
        # static
        self.color = [30, 30, 30]
        self.collision_ground = True
        self.allow_print = True
        self.id = id  # just for debugging
        # static hardcoded
        self.mass = 1.0
        # dynamic
        self.pt = np.array([x, y]).astype(float)  # current coordinate
        self.pt0 = np.array([x, y]).astype(float)  # previous coordinate

    def print(self):
        if(self.allow_print):
            print(f"point id={self.id}: pt={self.pt}. pt0={self.pt0}")


class line:
    def __init__(self, id, id_pt0, id_pt1, length):  # id is just for debugging
        # static
        self.color = [50, 50, 50]
        self.collision_ball = True
        self.id = id  # just for debugging
        self.id_pt0 = id_pt0
        self.id_pt1 = id_pt1
        self.length = length  # Desired length


class mussle:
    def __init__(self, id, id_pt0, id_pt1, length):  # id is just for debugging
        # static
        self.color = [250, 50, 50]
        self.id_pt0 = id_pt0
        self.id_pt1 = id_pt1
        self.id = id  # just for debugging
        # dynamic
        self.length = length  # Desired length
        self.minlength = length*0.5
        self.maxlength = length
        self.force = 0.1


class ptlnms:  # points+lines+mussles objects holder + some interclass methods
    def __init__(self):
        self.pts = []  # type: List[point]
        self.lns = []  # type: List[line]
        self.mss = []  # type: List[mussle]

    def add_pt(self, id, x, y):
        self.pts.append(point(id, x, y))

    def add_ln(self, id, id_pt0, id_pt1):
        length = self.get_length(id_pt0, id_pt1)
        self.lns.append(line(id, id_pt0, id_pt1, length))

    def add_ms(self, id, id_pt0, id_pt1):
        length = self.get_length(id_pt0, id_pt1)
        self.mss.append(mussle(id, id_pt0, id_pt1, length))
        self.mss[id].minlength=abs(self.get_length(id_pt0,id_pt0+1)-self.get_length(id_pt1,id_pt0+1))+1
        self.mss[id].maxlength=abs(self.get_length(id_pt0,id_pt0+1)+self.get_length(id_pt1,id_pt0+1))-1

    def get_length(self, id0, id1):
        return np.linalg.norm(self.pts[id1].pt - self.pts[id0].pt)

    def get_vector(self, id0, id1):
        return self.pts[id1].pt - self.pts[id0].pt

    def draw(self, screen):
        # head:
        pygame.draw.circle(screen, [50,50,50], ((self.pts[4].pt+1.2*(self.get_vector(4,5)))*fwc.scale).astype(int), int(15*fwc.scale))
        
        for ln in self.lns:
            pygame.draw.line(screen, ln.color, (self.pts[ln.id_pt0].pt*fwc.scale).astype(int),
                             (self.pts[ln.id_pt1].pt*fwc.scale).astype(int), int(10*fwc.scale))
        for pt in self.pts:
            pygame.draw.circle(screen, pt.color,
                               (pt.pt*fwc.scale).astype(int), int(5*fwc.scale))
