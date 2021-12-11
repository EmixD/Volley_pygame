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
    def __init__(self,ballindex):
        self.ball = fbl.ball(ballindex)
        self.ptlnms = fpptlnms.ptlnms()
        # standing hands up
        # self.ptlnms.add_pt(0, 180, 400)  # toe
        # self.ptlnms.add_pt(1, 200, 400)  # ankle
        # self.ptlnms.add_pt(2, 190, 350)  # knee
        # self.ptlnms.add_pt(3, 200, 300)  # hips
        # self.ptlnms.add_pt(4, 200, 200)  # shoulder
        # self.ptlnms.add_pt(5, 190, 160)  # elbow
        # self.ptlnms.add_pt(6, 200, 120)  # wrist
        # self.ptlnms.add_pt(7, 190, 100)  # fingertip

        # standing hands down
        # self.ptlnms.add_pt(0, 180, 400)  # toe
        # self.ptlnms.add_pt(1, 200, 400)  # ankle
        # self.ptlnms.add_pt(2, 190, 350)  # knee
        # self.ptlnms.add_pt(3, 200, 300)  # hips
        # self.ptlnms.add_pt(4, 200, 200)  # shoulder
        # self.ptlnms.add_pt(5, 190, 240)  # elbow
        # self.ptlnms.add_pt(6, 200, 280)  # wrist
        # self.ptlnms.add_pt(7, 190, 300)  # fingertip

        # standing hands down to the right
        # self.ptlnms.add_pt(0, 380, 400)  # toe
        # self.ptlnms.add_pt(1, 400, 400)  # ankle
        # self.ptlnms.add_pt(2, 390, 350)  # knee
        # self.ptlnms.add_pt(3, 400, 300)  # hips
        # self.ptlnms.add_pt(4, 400, 200)  # shoulder
        # self.ptlnms.add_pt(5, 395, 240)  # elbow
        # self.ptlnms.add_pt(6, 385, 275)  # wrist
        # self.ptlnms.add_pt(7, 385, 297)  # fingertip
        self.ptlnms.add_pt(0, 390+400, 400)  # ankle
        self.ptlnms.add_pt(1, 434+400, 400)  # ankle2
        self.ptlnms.add_pt(2, 370+400, 350)  # knee
        self.ptlnms.add_pt(3, 400+400, 358)  # knee2
        self.ptlnms.add_pt(4, 400+400, 300)  # hips

        self.ptlnms.add_pt(5, 400+400-10, 200)  # shoulder
        self.ptlnms.add_pt(6, 390+400-10, 250)  # elbow
        self.ptlnms.add_pt(7, 390+400-10, 250)  # elbow2
        self.ptlnms.add_pt(8, 345+400-10, 250)  # wrist
        self.ptlnms.add_pt(9, 345+400-10, 250)  # wrist2

        self.ptlnms.add_ln(0, 0, 2) #leglow
        self.ptlnms.add_ln(1, 1, 3) #leglow2
        self.ptlnms.add_ln(2, 2, 4) #leghi
        self.ptlnms.add_ln(3, 3, 4) #leghi2
        self.ptlnms.add_ln(4, 4, 5) #body
        self.ptlnms.add_ln(5, 5, 6) #armlow
        self.ptlnms.add_ln(6, 5, 7) #armlow2
        self.ptlnms.add_ln(7, 6, 8) #armhi
        self.ptlnms.add_ln(8, 7, 9) #armhi2
        
        self.ptlnms.lns[0].collision_ball = False
        self.ptlnms.lns[1].collision_ball = False
        self.ptlnms.lns[2].collision_ball = False
        self.ptlnms.lns[3].collision_ball = False
        self.ptlnms.lns[4].collision_ball = False
        self.ptlnms.lns[5].collision_ball = False
        self.ptlnms.lns[6].collision_ball = False

        self.ptlnms.add_ms(0, 0, 4) #ankle-hips
        self.ptlnms.add_ms(1, 1, 4) #ankle-hips2
        self.ptlnms.add_ms(2, 2, 5) #knee-shoulder
        self.ptlnms.add_ms(3, 3, 5) #knee-shoulder2
        self.ptlnms.add_ms(4, 4, 6) #hips-elbow
        self.ptlnms.add_ms(5, 4, 7) #hips-elbow2
        self.ptlnms.add_ms(6, 5, 8) #shoulder-wrist
        self.ptlnms.add_ms(7, 5, 9) #shoulder-wrist

    def draw(self, screen):
        self.ptlnms.draw(screen)
        self.ball.draw(screen)

    def move(self, dt):  # time is in game time
        if(self.ball.pt[1] >= fwc.ground-self.ball.rad):
            return
        for pt in self.ptlnms.pts:
            dr = pt.pt-pt.pt0
            pt.pt0 = pt.pt
            pt.pt = np.array(pt.pt0)+dr*fwc.airfriction
            pt.pt[1] = pt.pt[1]+fwc.gravity*dt**2
            if(pt.pt[1] > fwc.ground):  # ground hit
                pt.pt[1] = fwc.ground
                pt.pt0[1] = pt.pt[1]-dr[1]*0.5  # 0.5=groundbounce
                pt.pt0[0] = pt.pt[0]-(pt.pt[0]-pt.pt0[0])*0.05

        for ms in self.ptlnms.mss:
            dist = self.ptlnms.get_length(ms.id_pt0, ms.id_pt1)
            vect = self.ptlnms.get_vector(ms.id_pt0, ms.id_pt1)
            fract = (dist-ms.length)/ms.length/2*ms.force*1.0
            self.ptlnms.pts[ms.id_pt0].pt = self.ptlnms.pts[ms.id_pt0].pt+vect*fract
            self.ptlnms.pts[ms.id_pt1].pt = self.ptlnms.pts[ms.id_pt1].pt-vect*fract

        balldr = self.ball.pt-self.ball.pt0
        self.ball.pt0 = self.ball.pt
        self.ball.pt = np.array(self.ball.pt0)+balldr
        self.ball.pt[1] = self.ball.pt[1]+fwc.gravity*dt**2

        self.ball.nocollisions_yet = True
        for ln in self.ptlnms.lns:  # ball collision
            if(self.ball.nocollisions_yet and ln.collision_ball):
                line_norm = self.ptlnms.get_length(ln.id_pt0, ln.id_pt1)
                line_normalized = self.ptlnms.get_vector(
                    ln.id_pt0, ln.id_pt1)/line_norm
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
                    self.ball.nocollisions_yet = False
                    lineperpvectnorm = (self.ball.pt-pt_closest_on_line)/dist
                    shift = lineperpvectnorm*(self.ball.rad-dist+1)
                    self.ball.pt = self.ball.pt+shift
                    self.ball.pt0 = self.ball.pt-balldr+lineperpvectnorm * \
                        np.dot(balldr, lineperpvectnorm) * \
                        1.8  # fullbounce=2 nobounce=1

        # for pt in self.ptlnms.pts:
        #     if(pt.pt[1] > fwc.ground):  # ground hit
        #         pt.pt[1] = fwc.ground
        #         pt.pt0[1]=pt.pt[1]-

        for ln in self.ptlnms.lns:
            dist = self.ptlnms.get_length(ln.id_pt0, ln.id_pt1)
            vect = self.ptlnms.get_vector(ln.id_pt0, ln.id_pt1)
            fract = (dist-ln.length)/ln.length/2
            self.ptlnms.pts[ln.id_pt0].pt = self.ptlnms.pts[ln.id_pt0].pt+vect*fract
            self.ptlnms.pts[ln.id_pt1].pt = self.ptlnms.pts[ln.id_pt1].pt-vect*fract

    def get_current_score(self):
        if((self.ball.pt[0]-fwc.netposx) > 0):
            # not far enough. 0-500
            return 500-(self.ball.pt[0]-fwc.netposx)
        else:
            # far enough. 0-500
            return 800-abs(fwc.ground-self.ball.pt[1]-200)
        return

    def check_end_condition(self):
        return ((fwc.ground-self.ball.pt[1]) < 10) or ((self.ball.pt[0]-fwc.netposx) < 0)
