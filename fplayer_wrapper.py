# pwrapper should provide interface to deal with mussle changes due to a FIXED set of parameters.

from typing import List
import fplayer as fp
import numpy as np
import fworldconfig as fwc

class pwrapper:
    def __init__(self, id, params1):
        # static protected
        self.Ninput = 3
        # self.Ninterm1 = 2
        self.Noutput = 8
        # static
        self.player = fp.player(0)
        # dynamic
        self.params1 = params1.copy()  # matrix [Ninput,Nint1]
        # self.params2 = params2  # matrix [Nint1,Noutput]
        self.input = np.zeros(self.Ninput)
        self.output = np.zeros(self.Noutput)
        self.maxscore = -1000
        self.avgscore = -1000
        self.scores=[]
        self.avgscore_calculated=False
        self.id = id
        self.ballindex=0

    def reset_player(self,ballindex):
        self.player=fp.player(ballindex)
        self.maxscore=-1000
        self.ballindex=ballindex
    
    def set_avgscore(self,score):
        self.avgscore=score
        self.avgscore_calculated=True

    def update_outputs(self):
        self.input = np.array([
            self.player.ball.pt[0]-self.player.ptlnms.pts[3].pt[0],
            self.player.ball.pt[1]-self.player.ptlnms.pts[3].pt[1],
            fwc.netposx-self.player.ptlnms.pts[3].pt[0]
            ]
        )
        # self.interm1=self.input.dot(self.params1)
        self.output = self.input.dot(self.params1)
        self.process_outputs()

    def process_outputs(self):
        np.clip(self.output, -5, 5)
        self.update_mussle(0, self.output[0])
        self.update_mussle(1, self.output[1])
        self.update_mussle(2, self.output[2])
        self.update_mussle(3, self.output[3])
        # self.update_mussle(4, self.output[4])
        # self.update_mussle(5, self.output[5])

    def update_mussle(self, id, output):
        self.player.ptlnms.mss[id].length = np.clip(self.player.ptlnms.mss[id].length+output,
                                                    self.player.ptlnms.mss[id].minlength, self.player.ptlnms.mss[id].maxlength)

    def check_scores_then_simulation_complete(self):
        score = self.player.get_current_score()
        self.maxscore = max(score, self.maxscore)
        return self.player.check_end_condition()

    def save(self, fname):
        with open(fname, 'wb') as f:
            np.save(f, self.params1)

    def load(self, fname):
        with open(fname, 'rb') as f:
            self.params1 = np.load(f, allow_pickle=True)
