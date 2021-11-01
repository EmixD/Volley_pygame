import pygame
import time

import fplayer as fp
import fcommon as fcom 
import fworldconfig as fwc

# INIT
pygame.init()
fcom.init()

t=time.time_ns()
screen = pygame.display.set_mode([500*fwc.scale, 500*fwc.scale])
running = True
nsins=1000000000
frametime = 0.0001*nsins # 1/fps in ns
speed = 1.0
p1=fp.player()
skip_frames=10
# frametime = 0.02*nsins # 1/fps in ns
print("===============================")

def calc(t,dt):
    # print("---------frame")
    global p1
    p1.calc_forces()
    p1.calc_mussle_forces(t*speed/nsins)
    p1.apply_forces(dt*speed/nsins)
    p1.move_traps(dt*speed/nsins)
    


def redraw():
    global p1
    screen.fill((150, 150, 150))
    fcom.ground.draw(screen)
    p1.draw(screen)
    pygame.display.flip()

iskip=0
while running:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Exiting now...")
                running = False
        if ((time.time_ns()-t)>frametime):
            break
    dt=time.time_ns()-t
    calc(t,dt)
    if(iskip==skip_frames):
        redraw()
        iskip=-1
    t=time.time_ns()
    iskip=iskip+1

pygame.quit()
print("MAIN HALT")