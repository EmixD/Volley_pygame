import math

class mussles:
    def __init__(self,joint,func):
        self.joint=joint
        self.func=func #force(time)

def m_default(angle,t):
    return 10000

class m_hold_angle:
    def __init__(self,angle,mom):
        self.angle=angle #angle to hold
        self.mom=mom #force momentum
    def behaviour(self,angle,t):  
        return self.mom*math.sin(angle-self.angle)
    def set(self,angle,mom):
        self.angle=angle
        self.mom=mom
