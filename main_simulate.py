import time
import fplayers as fps


in_game_dt=0.1
in_game_tmax=100
update_mussles_every=10
print(f"estimated time is {in_game_dt*in_game_tmax/20} seconds")

tic = time.time()
fps.simulate(in_game_dt,update_mussles_every,in_game_tmax,False,0)
tac = time.time()
print('Operation took {} ms'.format((tac - tic) * 1e3))
print("MAIN HALT")