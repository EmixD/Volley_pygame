import math
from pickle import TRUE
from typing import List
import fplayer_wrapper as fpw
import numpy as np
import time
import pygame
import fworldconfig as fwc
import random

players = []  # type: List[fpw.pwrapper]
Nplayers = 0
iteration = 1
nSimulPerPlayer=10

def init(n):  # n should be even TODO: add check
    global players, Nplayers
    Nplayers = n
    players = []  # type: List[fpw.pwrapper]
    for i in range(Nplayers):
        players.append(fpw.pwrapper(i,
         np.zeros((3, 8)).astype(float)))
        #  2*np.random.rand(3, 8).astype(float)-1))

def sort(verb):
    global players
    players.sort(key=lambda x: x.avgscore, reverse=False)
    if(verb):
        for pl in players:
            print(f"Player# {pl.id}: MaxScore={pl.avgscore}")


def breed(verb):
    global players, Nplayers, iteration
    n2 = int(Nplayers/2)

    for i in range(n2):
        for _ in range(10):
            pars=players[n2+i].params1.copy()
            a1=random.randint(0,3-1)
            a2=random.randint(0,8-1)
            pars[a1,a2]=np.clip(pars[a1,a2]+0.01*(2*random.random()-1.0),-2,2)
            players[i] = fpw.pwrapper(
                iteration*100+i,
                pars
            )

    iteration = iteration+1
    if(verb):
        for pl in players:
            print(f"Player# {pl.id}: MaxScore={pl.avgscore}")

def simulate(dt, update_mussles_every, tmax, draw, screen, verb):
    global players, Nplayers
    if(draw):
        for pl in players:
            for s in range(nSimulPerPlayer):
                pl.reset_player(s)
                t = 0
                while not pl.check_scores_then_simulation_complete():
                    for _ in range(update_mussles_every):
                        t = t+dt
                        pl.player.move(dt)
                        
                        pygame.event.pump()
                        screen.fill((150, 150, 150))
                        pygame.draw.line(screen, (0, 0, 0), (int(0*fwc.scale), int(fwc.ground*fwc.scale)),
                                        (int(1000*fwc.scale), int(fwc.ground*fwc.scale)), int(3*fwc.scale))
                        pygame.draw.line(screen, (0, 0, 255), (int(fwc.netposx*fwc.scale), int(
                            fwc.ground*fwc.scale)), (int(fwc.netposx*fwc.scale), int(0*fwc.scale)), int(1*fwc.scale))
                        pl.player.draw(screen)
                        pygame.display.flip()
                        time.sleep(0.005)
                    pl.update_outputs()
                    if(t >= tmax):
                        if(verb):
                            print(f"Player# {pl.id}: Simulation timeout")
                        break
                if(verb):
                    print(f"Player# {pl.id}: MaxScore={pl.maxscore}")
    else:
        for pl in players:
            if(not pl.avgscore_calculated):
                scores=[]
                cumulscores=0
                for s in range(nSimulPerPlayer):
                    pl.reset_player(s)
                    t = 0
                    while not pl.check_scores_then_simulation_complete():
                        for _ in range(update_mussles_every):
                            t = t+dt
                            pl.player.move(dt)
                        pl.update_outputs()
                        if(t >= tmax):
                            if(verb):
                                print(f"Player# {pl.id}: Simulation timeout")
                            break
                    if(verb):
                        print(f"Player# {pl.id}: MaxScore={pl.maxscore}")                    
                    scores.append(pl.maxscore)
                    cumulscores=cumulscores+pl.maxscore
                pl.scores=scores.copy()
                # scores.sort()
                pl.set_avgscore(cumulscores/nSimulPerPlayer) 

def save():
    #TODO: transform to relatice path
    print("You should check that number of players is correct yourself!")
    for i,p in enumerate(players):
        p.save("C:/Users/Ivan/Desktop/[CURRENT]/Volley_pygame/save/f"+str(i))

def load():
    #TODO: transform to relatice path
    for i,p in enumerate(players):
        p.load("C:/Users/Ivan/Desktop/[CURRENT]/Volley_pygame/save/f"+str(i))