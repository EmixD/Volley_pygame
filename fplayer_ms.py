import pygame
from typing import List
import fworldconfig as fwc
import fplayer_pt as fppt


class mussle:
    mss = []  # type: List[mussle]

    def __init__(self, id, id_pt0, id_pt1):
        # static
        self.color = [250, 50, 50]
        self.id_pt0 = id_pt0
        self.id_pt1 = id_pt1
        #dynamic
        self.length = fppt.point.get_length(id_pt0, id_pt1)  # Desired length
        self.force = 0.1
        # init
        mussle.mss.append(self)

    def get_current_length(self):
        return fppt.point.get_length(self.id_pt0, self.id_pt1)
    
    def get_current_length0(self):
        return fppt.point.get_length0(self.id_pt0, self.id_pt1)
    
    def get_current_vector(self):
        return fppt.point.pts[self.id_pt1].pt-fppt.point.pts[self.id_pt0].pt
    
    def get_current_vector0(self):
        return fppt.point.pts[self.id_pt1].pt0-fppt.point.pts[self.id_pt0].pt0

    def draw(self, screen):
        pygame.draw.line(screen, self.color, (fppt.point.pts[self.id_pt0].pt*fwc.scale).astype(int), (fppt.point.pts[self.id_pt1].pt*fwc.scale).astype(int), int(2*self.force*fwc.scale))