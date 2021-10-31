import math


def m_default(angle,t):
    return 10000

class m_hold_angle:
    def __init__(self,angle,mom):
        self.angle=angle
        self.mom=mom
    def behaviour(self,angle,t):  
        if(abs(angle-self.angle)>0.1):
            return self.mom*(angle-self.angle)/abs(angle-self.angle)
        return (angle-self.angle)*self.mom
    def set(self,angle,mom):
        self.angle=angle
        self.mom=mom
