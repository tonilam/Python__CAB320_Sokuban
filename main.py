#### IMPORTANT: THIS FILE IS NOT USED IN MARKING !!!
####

from cab320_sokoban import Warehouse
from mySokobanSolver import *
import time

if __name__ == "__main__":
  problem_file = "./warehouses/warehouse_01.txt"


  """
  Create a Sokoban Puzzle
  """
  game = SokobanPuzzle(problem_file)

  print checkActions(problem_file, ['Left', 'Down', 'Down','Right', 'Up', 'Down'])

##  t0 = time.time()
##  sol_ts = astar_search(game)
##  t1 = time.time()
##  sp.print_solution(sol_ts)
