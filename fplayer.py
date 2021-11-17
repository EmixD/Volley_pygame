import numpy as np
from typing import List

import fplayer_pt as fppt
import fplayer_ln as fpln
import fplayer_ms as fpms
import fworldconfig as fwc
# import fworldconfig as fwc
# import fcommon as fcom


class player:
    def __init__(self):
        fppt.point(0, 180, 400)  # toe
        fppt.point(1, 200, 400)  # ankle
        fppt.point(2, 190, 350)  # knee
        fppt.point(4, 200, 300)  # shoulder
        fppt.point(3, 200, 200)  # hips
        fppt.point(5, 190, 160)  # elbow
        fppt.point(6, 200, 120)  # wrist
        fppt.point(7, 190, 100)  # fingertip

        fpln.line(0, 0, 1)
        fpln.line(1, 1, 2)
        fpln.line(2, 2, 3)
        fpln.line(3, 3, 4)
        fpln.line(4, 4, 5)
        fpln.line(5, 5, 6)
        fpln.line(6, 6, 7)

        fpms.mussle(0, 0, 2)
        fpms.mussle(1, 1, 3)
        fpms.mussle(2, 2, 4)
        fpms.mussle(3, 3, 5)
        fpms.mussle(4, 4, 6)
        fpms.mussle(5, 5, 7)

    def draw(self, screen):
        for ln in fpln.line.lns:
            ln.draw(screen)
        for pt in fppt.point.pts:
            pt.draw(screen)
        for ms in fpms.mussle.mss:
            ms.draw(screen)

    def move(self, dt):  # time is in game time
        for pt in fppt.point.pts:
            dr = (pt.pt-pt.pt0)*fwc.airfriction
            pt.pt0 = pt.pt                
            pt.pt = np.array(pt.pt0)+dr
            pt.pt[1] = pt.pt[1]+fwc.gravity*dt**2 

        for ms in fpms.mussle.mss:
            dist = ms.get_current_length()
            vect = ms.get_current_vector()
            fract = (dist-ms.length)/ms.length/2*ms.force*1.0
            fppt.point.pts[ms.id_pt0].pt = fppt.point.pts[ms.id_pt0].pt+vect*fract
            fppt.point.pts[ms.id_pt1].pt = fppt.point.pts[ms.id_pt1].pt-vect*fract
        
        for pt in fppt.point.pts:
            if(pt.pt[1] > 450):  # ground hit
                pt.pt[1] = 450
        
        for ln in fpln.line.lns:
            dist = ln.get_current_length()
            vect = ln.get_current_vector()
            fract = (dist-ln.length)/ln.length/2
            fppt.point.pts[ln.id_pt0].pt = fppt.point.pts[ln.id_pt0].pt+vect*fract
            fppt.point.pts[ln.id_pt1].pt = fppt.point.pts[ln.id_pt1].pt-vect*fract
    
    def get_current_score(self):
        return 450-fppt.point.pts[7].pt[1]
