import pygame
import time
import fplayers as fps
import fworldconfig as fwc


pygame.init()
fps.init(1)
screen = pygame.display.set_mode([1000*fwc.scale, 500*fwc.scale])


in_game_dt=0.1
in_game_tmax=100
update_mussles_every=10
print(f"estimated time is {in_game_dt*in_game_tmax/20 + 0.01*in_game_tmax/in_game_dt} seconds")

tic = time.time()
fps.simulate(in_game_dt,update_mussles_every,in_game_tmax,True,screen,True)
tac = time.time()
print('Operation took {} ms'.format((tac - tic) * 1e3))

pygame.quit()
print("MAIN HALT")
