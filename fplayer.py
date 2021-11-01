import numpy as np

import fmussle as fmus
import fplayer_trap as ftrap
import fplayer_joints as fjoi
import fworldconfig as fwc
import fcommon as fcom

class player:
    def __init__(self):
        trtoes=ftrap.trap(-10,0, 10,-10, 10,10, -10,10,   180,390,0,[50,50,50])
        trtoes.add_floor_collision(2)
        trtoes.add_floor_collision(3)
        trfoot=ftrap.trap(-10,-10, 10,-10, 10,10, -10,10,   200,390,0,[80,80,80])
        trfoot.add_floor_collision(2)
        trfoot.add_floor_collision(3)
        trleglow=ftrap.trap(-10,-25, 10,-25, 10,25, -10,25,  200,355,0,[50,50,50])
        trleghig=ftrap.trap(-10,-25, 10,-25, 10,25, -10,25,   200,305,0,[80,80,80])
        trbody=ftrap.trap(-15,-40, 15,-40, 15,40, -15,40,   200,240,0,[50,50,50])
        trbody.displayforces=True
        # trbody.printappliedforces=True
        trarmlow=ftrap.trap(-10,-20, 10,-20, 10,20, -10,20,     200,180,0,[80,80,80])
        trarmhig=ftrap.trap(-5,-20, 5,-20, 10,20, -10,20,    200,140,0,[50,50,50])
        trhand=ftrap.trap(-5,-10, 0,-10, 5,10, -5,10,    200,110,0,[80,80,80])

        self.traps=np.array([trtoes,trfoot,trleglow,trleghig,trbody,trarmlow,trarmhig,trhand])

        jtoesfoot=fjoi.joints(trtoes,1,2,trfoot,0,3)
        jfootleglow=fjoi.joints(trfoot,0,1,trleglow,3,2)
        jleglowleghig=fjoi.joints(trleglow,0,1,trleghig,3,2)
        jleghigbody=fjoi.joints(trleghig,0,1,trbody,3,2)
        # jleghigbody.printinfo=True
        jbodyarmlow=fjoi.joints(trbody,0,1,trarmlow,3,2)
        # jbodyarmlow.printinfo=True
        jarmlowarmhig=fjoi.joints(trarmlow,0,1,trarmhig,3,2)
        jarmhighand=fjoi.joints(trarmhig,0,1,trhand,3,2)
        self.joints=np.array([jtoesfoot,jfootleglow,jleglowleghig,jleghigbody,jbodyarmlow,jarmlowarmhig,jarmhighand])

        ang=20*3.1415926536/180.0 #RADIAN
        fo=1000000
        m1=fmus.m_hold_angle(ang,fo)
        m2=fmus.m_hold_angle(ang,fo)
        m3=fmus.m_hold_angle(ang,fo)
        m4=fmus.m_hold_angle(ang,fo)
        m5=fmus.m_hold_angle(ang,fo)
        m6=fmus.m_hold_angle(ang,fo)
        m7=fmus.m_hold_angle(ang,fo)

        mtoesfoot=fmus.mussles(jtoesfoot,m1.behaviour)
        mfootleglow=fmus.mussles(jfootleglow,m2.behaviour)
        mleglowleghig=fmus.mussles(jleglowleghig,m3.behaviour)
        mleggigbody=fmus.mussles(jleghigbody,m4.behaviour)
        mbodyarmlow=fmus.mussles(jbodyarmlow,m5.behaviour)
        marmlowarmhig=fmus.mussles(jarmlowarmhig,m6.behaviour)
        marmhighand=fmus.mussles(jarmhighand,m7.behaviour)
       
        self.mussles=[mtoesfoot,mfootleglow,mleglowleghig,mleggigbody,mbodyarmlow,marmlowarmhig,marmhighand]
    def calc_forces(self):
        for t in self.traps:
            t.update_pts_force()
            t.printstatus()
            t.force_cm=np.array([0,0]) #init
            t.force_mom=0 #init
            
            t.print("gravity:")
            t.add_force([0,fwc.g*t.m]) #gravity
            t.print("air friction:")
            t.add_force(-fwc.airfr*t.v)
            t.add_momentum(-fwc.airfrw*t.w)
            t.print("floor collision:")
            for p in t.col_floor: #floor collision+friction
                if(t.pts[p][1]>fcom.ground.y0):
                    if(t.printappliedforces):
                        print("floor collision: dr=",(t.pts[p][1]-fcom.ground.y0))
                    force=np.array([0,-fwc.groundforce*(t.pts[p][1]-fcom.ground.y0)])
                    t.add_force(force)
                    t.add_momentum_force(force,p)
                    t.print("floor collision: friction:")
                    t.add_force(-fwc.grfr*t.v)
                    t.add_momentum(-fwc.grfrw*t.w)
        for j in self.joints:
            j.print("-------------joint------------")
            if(j.printinfo):
                print("dr=",j.r(),"  force=+- ",j.force0())
            f0=j.force0()
            f1=j.force1()
            j.print("joint force:")
            j.traps[0].add_force(f0)
            j.traps[1].add_force(f1)
            j.traps[0].add_momentum_force(f0/2,j.p11)
            j.traps[0].add_momentum_force(f0/2,j.p12)
            j.traps[1].add_momentum_force(f1/2,j.p21)
            j.traps[1].add_momentum_force(f1/2,j.p22)
            j.print("joint friction:")
            v=j.traps[1].v-j.traps[0].v
            j.traps[0].add_force(v*fwc.jfr)
            j.traps[1].add_force(-v*fwc.jfr)
            w=j.traps[1].w-j.traps[0].w
            j.traps[0].add_momentum(w*fwc.jfrw)
            j.traps[1].add_momentum(-w*fwc.jfrw)
            j.print("==========")
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
        for j in self.joints:
            j.draw(screen)





