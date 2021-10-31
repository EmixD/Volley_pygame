import pygame
import time

import fplayer as fp
import fcommon as fcom 

# INIT
pygame.init()
fcom.init()

t=time.time_ns()
screen = pygame.display.set_mode([500, 500])
running = True
nsins=1000000000
frametime = 0.002*nsins # 1/fps in ns
speed = 0.5
p1=fp.player()
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
    global p1,gr
    screen.fill((255, 255, 255))
    fcom.ground.draw(screen)
    p1.draw(screen)
    pygame.display.flip()


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
    redraw()
    t=time.time_ns()

pygame.quit()
print("MAIN HALT")