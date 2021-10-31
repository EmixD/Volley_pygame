# This file is intended to define a vplayer class.
# It will be able to:
# 1. Define a player as a set of traps (relative,  static) and treir pos and rot.
#
#

import pygame
import math
import numpy as np
import mussle as mus



g=100.0 #gravity
groundforce=100.0
jforce=100.0
grfr=10
grfrw=0
airfr=0.05
airfrw=100
jfr=10
jfrw=500

class grounds: #unused for calc
    def __init__(self,y0,x0,x1):
        self.y0=y0
        self.x0=x0
        self.x1=x1
    def draw(self,screen):
        pygame.draw.line(screen, (0, 0, 0),(self.x0,self.y0),(self.x1,self.y0),2)

gr=grounds(400,0,500) #ground


class col_line:
    def __init__(self,x0,y0,x1,y1):
        self.x0=x0
        self.y0=y0
        self.x1=x1
        self.y1=y1

class trap:
    def __init__(self,x0,y0,x1,y1,x2,y2,x3,y3, xc,yc,rot,color):
        #static
        self.pts0=np.array([[x0,y0],[x1,y1],[x2,y2],[x3,y3]]).astype(float) #points relative to the center
        self.color=color #color for display
        #static hardcoded
        self.m=1.0 #mass
        self.i=100.0 #inertia moment
        self.frict=0.2 #lateral friction
        self.frictw=1.0 #rotational friction
        #init static
        self.col_ball=[] #collision lines (given by indexes of 2 pts)
        self.col_floor=[] #collision points (by index)
        #dynamic
        self.center=np.array([xc,yc]) #center of mass
        self.rot=rot #rotation
        #init dynamic
        self.force_cm=np.array([0.0,0.0]) #force that acts on the center of mass
        self.force_mom=0.0 #force momentum
        self.v=np.array([0.0,0.0]) #lateral speed
        self.w=0.0 #angular speed
        #temp
        self.pts =np.array([[x0,y0],[x1,y1],[x2,y2],[x3,y3]]).astype(float) #points (absolute, temporary variable)
        #control
        self.ptschanged=True
    #one-time calls
    def add_ball_collision(self,v0,v1):
        self.col_ball.append([v0,v1])
    def add_floor_collision(self,v0):
        self.col_floor.append(v0)
    #helpers
    def get_center(self): 
        return self.center
    def rotatepts(self,angrad): #should be applied before move
        c=np.array([0.0,0.0])
        si=math.sin(angrad)
        co=math.cos(angrad)
        for i,pt in enumerate(self.pts):
            r=pt-c
            xn=r[0]*co-r[1]*si
            yn=r[0]*si+r[1]*co
            self.pts[i][0]=c[0]+xn
            self.pts[i][1]=c[1]+yn
    def movepts(self,dr):
        for i,pt in enumerate(self.pts):
            self.pts[i]=pt+dr
    def update_pts(self):
        if(not self.ptschanged): 
            return
        print("1:",self.pts)
        self.pts=np.copy(self.pts0)
        print("2:",self.pts)
        self.rotatepts(self.rot)
        print("3:",self.pts," rot was",self.rot)
        self.movepts(self.get_center())
        print("4:",self.pts," dr was", self.get_center())
        self.ptschanged=False
    def move(self,dr):
        self.center+self.center+dr
        self.ptschanged=True
    def rotate(self,angrad):
        self.rot=self.rot+angrad
        self.ptschanged=True
    #forces
    def add_momentum_force(self,force,n_pt):
        rc=self.get_center()
        rpt=self.pts[n_pt]
        rr=rpt-rc
        dm=force[1]*rr[0]-force[0]*rr[1]
        self.force_mom=self.force_mom+dm
    def add_momentum(self,dm):
        self.force_mom=self.force_mom+dm
    def add_force(self,force):
        self.force_cm=self.force_cm+force
    #draw
    def draw(self,screen):
        self.update_pts()
        # print(self.pts)
        pygame.draw.polygon(screen,self.color, self.pts)
    def draw_col(self,screen):
        self.update_pts()
        for l in self.col_ball:
            pygame.draw.line(screen, (255, 0, 0),self.pts[l[0]],self.pts[l[1]])
        for v in self.col_floor:
            pygame.draw.circle(screen, (255, 0, 0),self.pts[v],3)
class joints:
    def __init__(self,trap1,p11,p12,trap2,p21,p22):
        self.traps=np.array([trap1,trap2])
        self.p11=p11
        self.p12=p12
        self.p21=p21
        self.p22=p22
        self.force=jforce
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
        # math.acos(np.dot(r0,r1)/np.linalg.norm(r0)/np.linalg.norm(r1))

class mussles:
    def __init__(self,joint,func):
        self.joint=joint
        self.func=func #force(time)

class player:
    def __init__(self):
        trtoes=trap(-10,0, 10,-10, 10,10, -10,10,   180,390,0,[50,50,50])
        trtoes.add_floor_collision(2)
        trtoes.add_floor_collision(3)
        trfoot=trap(-10,-10, 10,-10, 10,10, -10,10,   200,390,0,[20,20,20])
        trfoot.add_floor_collision(2)
        trfoot.add_floor_collision(3)
        trleglow=trap(-10,-25, 10,-25, 10,25, -10,25,  200,355,0,[20,20,100])
        trleghig=trap(-10,-25, 10,-25, 10,25, -10,25,   200,305,0,[20,20,50])
        trbody=trap(-15,-40, 15,-40, 15,40, -15,40,   200,240,0,[20,20,100])
        trarmlow=trap(-10,-20, 10,-20, 10,20, -10,20,     200,180,0,[20,20,150])
        trarmhig=trap(-5,-20, 5,-20, 10,20, -10,20,    200,140,0,[50,20,150])
        trhand=trap(-5,-10, 0,-10, 5,10, -5,10,    200,110,0,[20,20,200])

        self.traps=np.array([trtoes,trfoot,trleglow,trleghig,trbody,trarmlow,trarmhig,trhand])

        jtoesfoot=joints(trtoes,1,2,trfoot,0,3)
        jfootleglow=joints(trfoot,0,1,trleglow,3,2)
        jleglowleghig=joints(trleglow,0,1,trleghig,3,2)
        jleggigbody=joints(trleghig,0,1,trbody,3,2)
        jbodyarmlow=joints(trbody,0,1,trarmlow,3,2)
        jarmlowarmhig=joints(trarmlow,0,1,trarmhig,3,2)
        jarmhighand=joints(trarmhig,0,1,trhand,3,2)
        self.joints=np.array([jtoesfoot,jfootleglow,jleglowleghig,jleggigbody,jbodyarmlow,jarmlowarmhig,jarmhighand])

        m1=mus.m_hold_angle(0,10000)
        m2=mus.m_hold_angle(0,10000)
        m3=mus.m_hold_angle(0,10000)
        m4=mus.m_hold_angle(0,10000)
        m5=mus.m_hold_angle(0,10000)
        m6=mus.m_hold_angle(0,10000)
        m7=mus.m_hold_angle(0,10000)

        mtoesfoot=mussles(jtoesfoot,m1.behaviour)
        mfootleglow=mussles(jfootleglow,m2.behaviour)
        mleglowleghig=mussles(jleglowleghig,m3.behaviour)
        mleggigbody=mussles(jleggigbody,m4.behaviour)
        mbodyarmlow=mussles(jbodyarmlow,m5.behaviour)
        marmlowarmhig=mussles(jarmlowarmhig,m6.behaviour)
        marmhighand=mussles(jarmhighand,m7.behaviour)
       
        self.mussles=[mtoesfoot,mfootleglow,mleglowleghig,mleggigbody,mbodyarmlow,marmlowarmhig,marmhighand]
    def calc_forces(self):
        for t in self.traps:
            t.force_cm=np.array([0,g*t.m]) #init+gravity
            t.force_mom=0 #init
            t.add_force(-airfr*t.v)
            t.add_momentum(-airfrw*t.w)
            for p in t.col_floor: #floor collision+friction
                if(t.pts[p][1]>gr.y0):
                    force=np.array([0,-groundforce*(t.pts[p][1]-gr.y0)])
                    t.add_force(force)
                    t.add_momentum_force(force,p)
                    t.add_force(-grfr*t.v)
                    t.add_momentum(-grfrw*t.w)
        for j in self.joints:
            f0=j.force0()
            f1=j.force1()
            j.traps[0].add_force(f0)
            j.traps[1].add_force(f1)
            j.traps[0].add_momentum_force(f0/2,j.p11)
            j.traps[0].add_momentum_force(f0/2,j.p12)
            j.traps[1].add_momentum_force(f1/2,j.p21)
            j.traps[1].add_momentum_force(f1/2,j.p22)
            v=j.traps[1].v-j.traps[0].v
            j.traps[0].add_force(v*jfr)
            j.traps[1].add_force(-v*jfr)
            w=j.traps[1].w-j.traps[0].w
            j.traps[0].add_momentum(w*jfrw)
            j.traps[1].add_momentum(-w*jfrw)
    def calc_mussle_forces(self,t):
        for m in self.mussles:
            j=m.joint
            force=m.func(j.getangle(),t)
            j.traps[0].add_momentum(force)
            j.traps[1].add_momentum(-force)
    def apply_forces(self,dt):
        for t in self.traps:
            t.v=t.v+t.force_cm*dt/t.m
            t.w=t.w+t.force_mom*dt/t.i
    def move_traps(self,dt):
        for t in self.traps:
            t.move(t.v*dt)
            t.rotate(t.w*dt)
    def draw(self,screen):
        for t in self.traps:
            t.draw(screen)
            t.draw_col(screen)

p1=player()



