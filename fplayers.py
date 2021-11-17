import fplayer as fp

class pwrapper:
    def __init__(self):
        self.player=fp.player()
        self.maxscore=0
    def simulation_complete(self):
        score=self.player.get_current_score()
        self.maxscore=max(score,self.maxscore)
        if(score<=5):
            return True
        else:
            return False
    def simulate(self,dt,tmax):
        t=0
        while not self.simulation_complete():
            t=t+dt
            self.player.move(dt)
            if(t>=tmax):
                print("simulation timeout")
                break
        print(f"simulation complete. MaxScore={self.maxscore}")
        

        

