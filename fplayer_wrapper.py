# pwrapper should provide interface to deal with mussle changes due to a FIXED set of parameters.

from typing import List
import fplayer as fp
import numpy as np


class pwrapper:
    def __init__(self, params):
        # static protected
        self.Ninput = 2
        self.Noutput = 6
        # static
        self.player = fp.player()
        # dynamic
        self.params1 = params  # matrix [Ninput,Noutput]
        self.input = np.zeros(self.Ninput)
        self.output = np.zeros(self.Noutput)
        self.maxscore = 0

    def update_outputs(self):
        self.input = self.player.ball.pt
        self.output = self.input.dot(self.params1)
        self.process_outputs()

    def process_outputs(self):
        np.clip(self.output, -1, 1)
        self.update_mussle(0, self.output[0])
        self.update_mussle(1, self.output[1])
        self.update_mussle(2, self.output[2])
        self.update_mussle(3, self.output[3])
        self.update_mussle(4, self.output[4])
        self.update_mussle(5, self.output[5])

    def update_mussle(self, id, output):
        self.player.ptlnms.mss[id].length = np.clip(self.player.ptlnms.mss[id].length+output,
                                                    self.player.ptlnms.mss[id].minlength, self.player.ptlnms.mss[id].maxlength)

    def check_scores_then_simulation_complete(self):
        score = self.player.get_current_score()
        self.maxscore = max(score, self.maxscore)
        if(score <= 20):
            return True
        else:
            return False
