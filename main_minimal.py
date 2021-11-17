import pygame
import time
import fplayer as fp
import fworldconfig as fwc


pygame.init()
screen = pygame.display.set_mode([500*fwc.scale, 500*fwc.scale])

player1 = fp.player()

# tic = time.time()
for _ in range(1000):
    player1.move(0.1)
    screen.fill((150, 150, 150))
    pygame.draw.line(screen, (0, 0, 0),(int(0*fwc.scale),int(450*fwc.scale)),(int(500*fwc.scale),int(450*fwc.scale)),int(2*fwc.scale))
    player1.draw(screen)
    pygame.display.flip()
    time.sleep(0.01)
# tac = time.time()
# print('Operation took {} ms'.format((tac - tic) * 1e3))


pygame.quit()
print("MAIN HALT")
