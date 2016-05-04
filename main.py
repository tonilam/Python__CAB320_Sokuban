#### IMPORTANT: THIS FILE IS NOT USED IN MARKING !!!
####

from cab320_sokoban import Warehouse
from mySokobanSolver import *
import time

if __name__ == "__main__":
  for i in range(1,58,2):
    if i != 101 and i != 167:
      if i < 10:
          problem_file = "./warehouses/warehouse_0"+str(i)+".txt"
      else:
          problem_file = "./warehouses/warehouse_"+str(i)+".txt"
      print "============================== warehouse "+str(i)+" =============================="

      print "Checking solveSokoban_elementary()"
      print solveSokoban_elementary(problem_file, 10)


  """
  Create a Sokoban Puzzle
  """
##
##  print "Checking checkActions()"
##  print checkActions(problem_file, ['Left', 'Up', 'Left', 'Down'])
##
##  print "Checking tabooCells()"
##  print tabooCells(problem_file)

  

##  t0 = time.time()
##  sol_ts = astar_search(game)
##  t1 = time.time()
##  sp.print_solution(sol_ts)
