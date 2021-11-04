import fplayer as fp

class pwrapper:
    def __init__(self):
        self.player=fp.player()
    #simulation
    def terminate(self):
        if(self.player.get_hand_height()>350):
            return True
        else:
            return False
    def simulate(self,dt):
        while not self.terminate():
            self.player.calc_and_move(dt)
        print("simulation complete")
        

