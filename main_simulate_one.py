import math
import pygame
import time

import fplayer as fp
import fplayer_wrapper as fpw
import fcommon as fcom 
import fworldconfig as fwc

# INIT
# pygame.init()
fcom.init()

# screen = pygame.display.set_mode([500*fwc.scale, 500*fwc.scale])

nsins=1000000000

frametime = 0.1*nsins # 1/fps in ns. Determines REDRAW fps
speed = 1.0 #Game simulation speed
calc_per_frame=10 #calculations per frame. Needs to be high for high speed and for low fps

# Overrides to set krakenval:
# frametime = (10.0**6)/speed*calc_per_frame
# speed = (10.0**6)/frametime*calc_per_frame
calc_per_frame = int(1/(10.0**6)*frametime*speed)


pw=fpw.pwrapper()
# pw.simulate(frametime*speed/nsins/calc_per_frame)
for a in range(10000):
    pw.player.calc_and_move(frametime*speed/nsins/calc_per_frame)
# screen.fill((150, 150, 150))
# fcom.ground.draw(screen)
# pw.player.draw(screen)
# pygame.display.flip()

# time.sleep(5)
# pygame.quit()
# print("MAIN HALT")