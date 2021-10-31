import numpy as np
import mussle as mus
import player_trap as tr
import player_joints as jo
import worldconfig as wc
import common as com


class col_line:
    def __init__(self,x0,y0,x1,y1):
        self.x0=x0
        self.y0=y0
        self.x1=x1
        self.y1=y1

class mussles:
    def __init__(self,joint,func):
        self.joint=joint
        self.func=func #force(time)

class player:
    def __init__(self):
        trtoes=tr.trap(-10,0, 10,-10, 10,10, -10,10,   180,390,0,[50,50,50])
        trtoes.add_floor_collision(2)
        trtoes.add_floor_collision(3)
        trfoot=tr.trap(-10,-10, 10,-10, 10,10, -10,10,   200,390,0,[20,20,20])
        trfoot.add_floor_collision(2)
        trfoot.add_floor_collision(3)
        trleglow=tr.trap(-10,-25, 10,-25, 10,25, -10,25,  200,355,0,[20,20,100])
        trleghig=tr.trap(-10,-25, 10,-25, 10,25, -10,25,   200,305,0,[20,20,50])
        trbody=tr.trap(-15,-40, 15,-40, 15,40, -15,40,   200,240,0,[20,20,100])
        trarmlow=tr.trap(-10,-20, 10,-20, 10,20, -10,20,     200,180,0,[20,20,150])
        trarmhig=tr.trap(-5,-20, 5,-20, 10,20, -10,20,    200,140,0,[50,20,150])
        trhand=tr.trap(-5,-10, 0,-10, 5,10, -5,10,    200,110,0,[20,20,200])

        self.traps=np.array([trtoes,trfoot,trleglow,trleghig,trbody,trarmlow,trarmhig,trhand])

        jtoesfoot=jo.joints(trtoes,1,2,trfoot,0,3)
        jfootleglow=jo.joints(trfoot,0,1,trleglow,3,2)
        jleglowleghig=jo.joints(trleglow,0,1,trleghig,3,2)
        jleggigbody=jo.joints(trleghig,0,1,trbody,3,2)
        jbodyarmlow=jo.joints(trbody,0,1,trarmlow,3,2)
        jarmlowarmhig=jo.joints(trarmlow,0,1,trarmhig,3,2)
        jarmhighand=jo.joints(trarmhig,0,1,trhand,3,2)
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
            t.force_cm=np.array([0,wc.g*t.m]) #init+gravity
            t.force_mom=0 #init
            t.add_force(-wc.airfr*t.v)
            t.add_momentum(-wc.airfrw*t.w)
            for p in t.col_floor: #floor collision+friction
                if(t.pts[p][1]>com.ground.y0):
                    force=np.array([0,-wc.groundforce*(t.pts[p][1]-com.ground.y0)])
                    t.add_force(force)
                    t.add_momentum_force(force,p)
                    t.add_force(-wc.grfr*t.v)
                    t.add_momentum(-wc.grfrw*t.w)
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
            j.traps[0].add_force(v*wc.jfr)
            j.traps[1].add_force(-v*wc.jfr)
            w=j.traps[1].w-j.traps[0].w
            j.traps[0].add_momentum(w*wc.jfrw)
            j.traps[1].add_momentum(-w*wc.jfrw)
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





