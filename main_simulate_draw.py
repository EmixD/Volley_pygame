import pygame
import time
import fplayers as fps
import fworldconfig as fwc


pygame.init()
screen = pygame.display.set_mode([500*fwc.scale, 500*fwc.scale])


in_game_dt=0.1
in_game_tmax=100
update_mussles_every=10
print(f"estimated time is {in_game_dt*in_game_tmax/20 + 0.01*in_game_tmax/in_game_dt} seconds")

tic = time.time()
fps.simulate(in_game_dt,update_mussles_every,in_game_tmax,True,screen)
tac = time.time()
print('Operation took {} ms'.format((tac - tic) * 1e3))

# player1 = fp.player()

# screen.fill((150, 150, 150))
# player1.draw(screen)
# pygame.display.flip()
# time.sleep(5)

# tic = time.time()
# for _ in range(400):
#     player1.move(0.1)
#     screen.fill((150, 150, 150))
#     pygame.draw.line(screen, (0, 0, 0),(int(0*fwc.scale),int(fwc.ground*fwc.scale)),(int(500*fwc.scale),int(fwc.ground*fwc.scale)),int(3*fwc.scale))
#     pygame.draw.line(screen, (0, 0, 255),(int(fwc.netposx*fwc.scale),int(fwc.ground*fwc.scale)),(int(fwc.netposx*fwc.scale),int(0*fwc.scale)),int(1*fwc.scale))
#     player1.draw(screen)
#     pygame.display.flip()
#     time.sleep(0.01)

# tac = time.time()
# print('Operation took {} ms'.format((tac - tic) * 1e3))


pygame.quit()
print("MAIN HALT")
