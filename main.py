import math
import pygame
import time

import fplayer as fp
import fcommon as fcom 
import fworldconfig as fwc

# INIT
pygame.init()
fcom.init()
pygame.font.init()
font = pygame.font.Font(pygame.font.get_default_font(), 12*fwc.scale)

t=time.time_ns()
t0=t #for prettier time display
screen = pygame.display.set_mode([500*fwc.scale, 700*fwc.scale])
running = True
nsins=1000000000
frametime = 0.02*nsins # 1/fps in ns. Determines REDRAW fps
speed = 26.7 #Game simulation speed
calc_per_frame=18 #calculations per frame. Needs to be high for high speed and for low fps
p1=fp.player()

# frametime = 0.02*nsins # 1/fps in ns
print("===============================")
print("calcstepfactor=",int(10*math.log10(speed*frametime/calc_per_frame))/10.0," (7.4=kraken)")
def calc(t,dt):
    # print("-calc",(time.time_ns()-t0)/nsins)
    global p1
    p1.calc_forces()
    p1.calc_mussle_forces(t*speed/nsins)
    p1.apply_forces(dt*speed/nsins)
    p1.move_traps(dt*speed/nsins)
    


def redraw(real_frametime):
    # print("=draw",(time.time_ns()-t0)/nsins)
    global p1
    screen.fill((150, 150, 150))
    fcom.ground.draw(screen)
    p1.draw(screen)

    text_surface = font.render('DFT={0}, suggested calc_per_frame={1}'.format(real_frametime/nsins,int(suggest)), True, (0, 0, 0))
    screen.blit(text_surface, dest=(0,0))
    pygame.display.flip()

suggest=0
while running:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Exiting now...")
                running = False
        if ((time.time_ns()-t)>frametime):
            #need to redraw
            redraw(time.time_ns()-t)
            #sync in-game and real times
            t=time.time_ns() # in-game and real time of last redraw
            break 
    for i in range(calc_per_frame):
        tcurr=t+frametime*(i+1)/calc_per_frame
        calc(tcurr,frametime/calc_per_frame)
    tcomplete=time.time_ns()
    suggest=frametime/(tcomplete-t)*calc_per_frame
    # print("-done",(tcomplete-t0)/nsins)


pygame.quit()
print("MAIN HALT")