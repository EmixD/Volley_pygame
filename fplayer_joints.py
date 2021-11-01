import math
import numpy as np
import pygame

import fworldconfig as fwc

class joints:
    def __init__(self,trap1,p11,p12,trap2,p21,p22):
        self.traps=np.array([trap1,trap2])
        self.p11=p11
        self.p12=p12
        self.p21=p21
        self.p22=p22
        self.force=fwc.jforce
        self.printinfo=False
    def getr0(self):
        return (self.traps[0].pts[self.p11]+self.traps[0].pts[self.p12])/2
    def getr1(self):
        return (self.traps[1].pts[self.p21]+self.traps[1].pts[self.p22])/2
    def r(self):
        r0=self.getr0()
        r1=self.getr1()
        return r1-r0
    def force0(self):
        return self.force*self.r()
    def force1(self):
        return -self.force*self.r()
    def getangle(self):
        r0=self.traps[0].pts[self.p12]-self.traps[0].pts[self.p11]
        r1=self.traps[1].pts[self.p22]-self.traps[1].pts[self.p21]
        return math.atan2(r1[1],r1[0])-math.atan2(r0[1],r0[0])
    def draw(self,screen):
        pygame.draw.circle(screen, (0, 0, 255),self.getr0()*fwc.scale,1*fwc.scale)
        pygame.draw.circle(screen, (0, 255, 0),self.getr1()*fwc.scale,1*fwc.scale)
    def print(self,text):
        if(self.printinfo):
            print(text)
