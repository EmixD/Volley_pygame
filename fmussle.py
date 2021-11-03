import math

class mussles:
    def __init__(self,joint,func):
        self.joint=joint
        self.func=func #force(time)

class m_hold_angle: 
    def __init__(self,angle,mom):
        self.angle=angle #angle to hold
        self.mom=mom #force momentum
    def behaviour(self,angle):  
        return self.mom*math.sin(angle-self.angle)
    def set(self,angle,mom):
        self.angle=angle
        self.mom=mom
