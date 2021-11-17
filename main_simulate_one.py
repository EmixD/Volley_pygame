import time
import fplayers as fps


in_game_dt=0.1
in_game_tmax=100
print(f"estimated time is {in_game_dt*in_game_tmax/20} seconds")

players=fps.pwrapper()
tic = time.time()
players.simulate(in_game_dt,in_game_tmax)
tac = time.time()
print('Operation took {} ms'.format((tac - tic) * 1e3))
print("MAIN HALT")