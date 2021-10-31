from math import sin
import pygame
import time
import game as g



pygame.init()

# INIT

t=time.time_ns()
screen = pygame.display.set_mode([500, 500])
running = True
nsins=1000000000
frametime = 0.02*nsins # 1/fps in ns
speed = 0.5
# frametime = 0.02*nsins # 1/fps in ns
print("===============================")

def calc(t,dt):
    # print("---------frame")
    global p1
    g.p1.calc_forces()
    g.p1.calc_mussle_forces(t*speed/nsins)
    g.p1.apply_forces(dt*speed/nsins)
    # p1.apply_friction(dt/nsins)
    g.p1.move_traps(dt*speed/nsins)
    


def redraw():
    global p1,gr
    screen.fill((255, 255, 255))
    g.gr.draw(screen)
    g.p1.draw(screen)
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