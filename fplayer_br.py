# This is the brain of a player
# Inputs:
# Ball position - 0=floor(y=ground) 1=ceiling(y=0)
# Ball speed - const * ball_dr/dt
# 
# Outputs:
# For every mussle: deltaforce, deltalength

from typing import List
import fplayer_pt as fppt
import numpy as np


class brain:
    brs = []  # type: List[brain]

    def __init__(self):
        self.cells=np.zeros(10)
        brain.brs.append(self)

    def update_mussles(self):
        pass
