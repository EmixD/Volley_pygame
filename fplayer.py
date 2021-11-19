# player->{lines/points/current mussles}
# 
# Every simulated player is an object of player class. 
# Every player obj has it's own set of lines/points/mussles
# Player simulates only microphysics (i.e. with fixed mussle properties). Mussle changes should be done on the player-wrapper level.

import numpy as np
from typing import List

import fplayer_pt_ln_ms as fpptlnms
import fplayer_bl as fbl
import fworldconfig as fwc


class player:
    def __init__(self):
        self.ball=fbl.ball()
        self.ptlnms=fpptlnms.ptlnms()
        self.ptlnms.add_pt(0, 180, 400)  # toe
        self.ptlnms.add_pt(1, 200, 400)  # ankle
        self.ptlnms.add_pt(2, 190, 350)  # knee
        self.ptlnms.add_pt(4, 200, 300)  # shoulder
        self.ptlnms.add_pt(3, 200, 200)  # hips
        self.ptlnms.add_pt(5, 190, 160)  # elbow
        self.ptlnms.add_pt(6, 200, 120)  # wrist
        self.ptlnms.add_pt(7, 190, 100)  # fingertip

        self.ptlnms.add_ln(0, 0, 1)
        self.ptlnms.add_ln(1, 1, 2)
        self.ptlnms.add_ln(2, 2, 3)
        self.ptlnms.add_ln(3, 3, 4)
        self.ptlnms.add_ln(4, 4, 5)
        self.ptlnms.add_ln(5, 5, 6)
        self.ptlnms.add_ln(6, 6, 7)

        self.ptlnms.add_ms(0, 0, 2)
        self.ptlnms.add_ms(1, 1, 3)
        self.ptlnms.add_ms(2, 2, 4)
        self.ptlnms.add_ms(3, 3, 5)
        self.ptlnms.add_ms(4, 4, 6)
        self.ptlnms.add_ms(5, 5, 7)

    def draw(self, screen):
        self.ptlnms.draw(screen)
        self.ball.draw(screen)

    def move(self, dt):  # time is in game time
        if(self.ball.pt[1]>=fwc.ground-self.ball.rad):
            return
        for pt in self.ptlnms.pts:
            dr = pt.pt-pt.pt0
            pt.pt0 = pt.pt
            pt.pt = np.array(pt.pt0)+dr*fwc.airfriction
            pt.pt[1] = pt.pt[1]+fwc.gravity*dt**2
            if(pt.pt[1] > fwc.ground):  # ground hit
                pt.pt[1] = fwc.ground
                pt.pt0[1]=pt.pt[1]-dr[1]*0.5 #0.5=groundbounce

        for ms in self.ptlnms.mss:
            dist = self.ptlnms.get_length(ms.id_pt0,ms.id_pt1)
            vect = self.ptlnms.get_vector(ms.id_pt0,ms.id_pt1)
            fract = (dist-ms.length)/ms.length/2*ms.force*1.0
            self.ptlnms.pts[ms.id_pt0].pt = self.ptlnms.pts[ms.id_pt0].pt+vect*fract
            self.ptlnms.pts[ms.id_pt1].pt = self.ptlnms.pts[ms.id_pt1].pt-vect*fract

        balldr = self.ball.pt-self.ball.pt0
        self.ball.pt0 = self.ball.pt
        self.ball.pt = np.array(self.ball.pt0)+balldr
        self.ball.pt[1] = self.ball.pt[1]+fwc.gravity*dt**2

        self.ball.nocollisions_yet=True
        for ln in self.ptlnms.lns:  # ball collision
            if(self.ball.nocollisions_yet and ln.collision_ball):
                line_norm = self.ptlnms.get_length(ln.id_pt0,ln.id_pt1)
                line_normalized = self.ptlnms.get_vector(ln.id_pt0,ln.id_pt1)/line_norm
                line_pt0 = self.ptlnms.pts[ln.id_pt0].pt
                line_pt0_to_ball = self.ball.pt-line_pt0
                projlen = np.dot(line_pt0_to_ball, line_normalized)

                if(projlen < 0):
                    projlen = 0
                if(projlen > line_norm):
                    projlen = line_norm

                pt_closest_on_line = line_pt0+line_normalized*projlen

                dist = np.linalg.norm(self.ball.pt-pt_closest_on_line)
                if(dist < self.ball.rad):
                    self.ball.nocollisions_yet=False
                    lineperpvectnorm = (self.ball.pt-pt_closest_on_line)/dist
                    shift = lineperpvectnorm*(self.ball.rad-dist+1)
                    self.ball.pt = self.ball.pt+shift
                    self.ball.pt0 = self.ball.pt+balldr*0.5

        # for pt in self.ptlnms.pts:
        #     if(pt.pt[1] > fwc.ground):  # ground hit
        #         pt.pt[1] = fwc.ground
        #         pt.pt0[1]=pt.pt[1]-

        for ln in self.ptlnms.lns:
            dist = self.ptlnms.get_length(ln.id_pt0,ln.id_pt1)
            vect = self.ptlnms.get_vector(ln.id_pt0,ln.id_pt1)
            fract = (dist-ln.length)/ln.length/2
            self.ptlnms.pts[ln.id_pt0].pt = self.ptlnms.pts[ln.id_pt0].pt+vect*fract
            self.ptlnms.pts[ln.id_pt1].pt = self.ptlnms.pts[ln.id_pt1].pt-vect*fract

    def get_current_score(self):
        return fwc.ground-self.ball.pt[1]
