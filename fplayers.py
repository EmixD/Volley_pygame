from typing import List
import fplayer_wrapper as fpw
import numpy as np
import time
import pygame
import fworldconfig as fwc



def simulate(dt, update_mussles_every, tmax, draw, screen):
    players = []  # type: List[fpw.pwrapper]

    players.append(fpw.pwrapper(-0.01*np.ones((2, 6))))

    for pl in players:
        t = 0
        while not pl.check_scores_then_simulation_complete():
            for _ in range(update_mussles_every):
                t = t+dt
                pl.player.move(dt)
                if(draw):
                    screen.fill((150, 150, 150))
                    pygame.draw.line(screen, (0, 0, 0),(int(0*fwc.scale),int(fwc.ground*fwc.scale)),(int(500*fwc.scale),int(fwc.ground*fwc.scale)),int(3*fwc.scale))
                    pygame.draw.line(screen, (0, 0, 255),(int(fwc.netposx*fwc.scale),int(fwc.ground*fwc.scale)),(int(fwc.netposx*fwc.scale),int(0*fwc.scale)),int(1*fwc.scale))
                    pl.player.draw(screen)
                    pygame.display.flip()
                    time.sleep(0.01)
            pl.update_outputs()
            if(t >= tmax):
                print(f"{pl}: Simulation timeout")
                break
        print(f"{pl}: MaxScore={pl.maxscore}")
