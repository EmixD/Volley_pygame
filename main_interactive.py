import pygame
import time

import fplayers as fps
import fworldconfig as fwc


pygame.init()
fps.init(10)
print("Init complete.")
screen = pygame.display.set_mode([1000*fwc.scale, 500*fwc.scale])
in_game_dt = 0.2
in_game_tmax = 100
update_mussles_every = 20


running = True
while(running):
    pygame.display.iconify()
    print("""===================================
    WAITING FOR INPUT:
    1 - print current generation
    2 - draw current generation
    5 - one full cycle 
    6 - 10x5
    7 - 50x5
    77 - 100x5
    81 - save to file
    82 - load from file
    9 - exit""")
    command = input()
    print("-----------------------------------")
    # command="2"
    if(command == "1"):
        for pl in fps.players:
            print(f"Player [{pl.id}]: {pl.avgscore}")
    elif(command == "2"):
        fps.simulate(in_game_dt, update_mussles_every,
                     in_game_tmax, True, screen, True)
    # elif(command == "3"):
    #     fps.sort(True)
    #     print("DONE. Next: 4")
    # elif(command == "4"):
    #     fps.breed(True)
    #     print("DONE. Next: 1 2 5 6 7")
    elif(command == "5"):
        fps.save()
        fps.simulate(in_game_dt, update_mussles_every,
                     in_game_tmax, False, 0, False)
        fps.sort(False)
        fps.breed(False)
        print("DONE")
    elif(command == "6"):
        fps.save()
        for o in range(10):
            fps.simulate(in_game_dt, update_mussles_every,
                        in_game_tmax, False, 0, False)
            fps.sort(False)
            if(o<9):
                fps.breed(False)
            print(o+1,fps.players[-1].avgscore)
        print("DONE")
    elif(command == "7"):
        fps.save()
        for o in range(50):
            fps.simulate(in_game_dt, update_mussles_every,
                        in_game_tmax, False, 0, False)
            fps.sort(False)
            if(o<49):
                fps.breed(False)
            print(o+1,fps.players[-1].avgscore)
        print("DONE")
    elif(command == "77"):
        fps.save()
        for o in range(100):
            fps.simulate(in_game_dt, update_mussles_every,
                        in_game_tmax, False, 0, False)
            fps.sort(False)
            if(o<99):
                fps.breed(False)
            print(o+1,fps.players[-1].avgscore)
        print("DONE")
    elif(command == "81"):
        fps.save()
    elif(command == "82"):
        fps.load()
    elif(command == "9"):
        running = False

pygame.quit()
print("MAIN HALT")
