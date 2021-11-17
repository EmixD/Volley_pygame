import pygame
from typing import List
import fworldconfig as fwc
import fplayer_pt as fppt


class line:
    lns = []  # type: List[line]

    def __init__(self, id, id_pt0, id_pt1):
        # static
        self.color = [50, 50, 50]
        self.collision_ball = True
        self.id_pt0 = id_pt0
        self.id_pt1 = id_pt1
        self.length = fppt.point.get_length(id_pt0, id_pt1)  # Desired length
        # init
        line.lns.append(self)

    def get_current_length(self):
        return fppt.point.get_length(self.id_pt0, self.id_pt1)
    
    def get_current_length0(self):
        return fppt.point.get_length0(self.id_pt0, self.id_pt1)
    
    def get_current_vector(self):
        return fppt.point.pts[self.id_pt1].pt-fppt.point.pts[self.id_pt0].pt
    
    def get_current_vector0(self):
        return fppt.point.pts[self.id_pt1].pt0-fppt.point.pts[self.id_pt0].pt0

    def draw(self, screen):
        pygame.draw.line(screen, self.color, (fppt.point.pts[self.id_pt0].pt*fwc.scale).astype(int), (fppt.point.pts[self.id_pt1].pt*fwc.scale).astype(int), int(10*fwc.scale))