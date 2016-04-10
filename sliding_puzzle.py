
##    Last modified 2015-03-08
##    by f.maire@qut.edu.au

                     
#from cab320_search_SOLUTION import *  # Search module adapted from AIMA for CAB320
from cab320_search import *  # Search module adapted from AIMA for CAB320
import random
import time

# An on-line applet for the sliding puzzle   http://mypuzzle.org/sliding

class Sliding_puzzle(Problem):
    """
    The tiles are in a a grid with self.nr rows and self.nc columns.
    A state is represented as permutation of the first nr x nc integers.
    The position of zero in this list represent the blank tile.
    The tiles are read row by row.
    For example, for a 3x3 grid,  the list (3,1,2,6,4,5,7,8,0) corresponds to 
	312
	645
	78*
    The actions are 'U','D','L' and 'R'  (move the blank tile up, down, left  right)
    """

    def actions(self, state):
        # index of the blank
        i_blank = state.index(0)
        L = []  # list of legal actions
        # UP: if blank not on top row, swap it with tile above it
        if i_blank >= self.nc:
            L.append('U')
        # DOWN: If blank not on bottom row, swap it with tile below it
        if i_blank < self.nc*(self.nr-1):
            L.append('D')
        # LEFT: If blank not in left column, swap it with tile to the left
        if i_blank % self.nc > 0:
            L.append('L')
        # RIGHT: If blank not on right column, swap it with tile to the right
        if i_blank % self.nc < self.nc-1:
            L.append('R')
        return L

    def result(self, state, action):
        """
        Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state).
        """
        # index of the blank
##        next_state = state[:] # Note that  next_state=state   would simply create an alias
        next_state = list(state)# Note that  next_state=state   would simply create an alias
        i_blank = state.index(0)
        assert action in self.actions(state)  # defensive programming!
        # UP: if blank not on top row, swap it with tile above it
        if action == 'U':
            i_swap = i_blank - self.nc
        # DOWN: If blank not on bottom row, swap it with tile below it
        if action == 'D':
            i_swap = i_blank + self.nc
        # LEFT: If blank not in left column, swap it with tile to the left
        if action == 'L':
            i_swap = i_blank - 1
        # RIGHT: If blank not on right column, swap it with tile to the right
        if action == 'R':
            i_swap = i_blank + 1
        next_state[i_swap], next_state[i_blank] = next_state[i_blank], next_state[i_swap] 
##        return next_state
        return tuple(next_state) # use tuple to make the state hashable

    def random_state(self, s, n=20):
        """
        Returns a state reached by N random actions generated by
        successor_function starting from state s
        """
        for i in xrange(n):
            a = random.choice(self.actions(s))
            s = self.result(s,a)
        return s
    
    def __init__(self,
                 nr = 3, # number of rows
                 nc = 3, # number of columns
                 goal = None, # goal state 
                 initial = None, # initial state
                 N = 20 # number of random moves from goal state
                        # if no initial state given
                 ): 
        # Problem.__init__(self, initial, goal)
        self.nr , self.nc = nr , nc
        if goal is None:
            self.goal = range(nr*nc)
        else:
            assert set(goal)==set(range(nr*nc))
            self.goal = goal
        if initial:
            self.initial = initial
        else:
            self.initial = self.random_state(self.goal, N)
        self.initial = tuple(self.initial)
        self.goal = tuple(self.goal)
    ## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        
    def print_solution(self, goal_node):
        """
            Shows solution represented by a specific goal node.
            For example, goal node could be obtained by calling 
                goal_node = breadth_first_tree_search(problem)
        """
        # path is list of nodes from initial state (root of the tree)
        # to the goal_node
        path = goal_node.path()
        # print the solution
        print "Solution takes {0} steps from the initial state\n".format(len(path)-1)
        self.print_state(path[0].state)
        print "to the goal state\n"
        self.print_state(path[-1].state)
        print "Below is the sequence of moves\n"
        for node in path:
            self.print_node(node)

    def print_node(self, node):
        """Print the action and resulting state"""
        if node.action:
            print "Move "+node.action
        self.print_state(node.state)

    def print_state(self, s):
        """Print the state s"""
        for ri in xrange(self.nr):
            print '\t',
            for ci in xrange(self.nc):
                t = s[ri*self.nc+ci]
                if self.nr*self.nc<10:
                    if t>0:
                        print t,
                    else:
                        print ' ',
                elif self.nr*self.nc<100:
                    if t>0:
                        print '{:>2}'.format(t),
                    else:
                        print ' '*2,
                elif self.nr*self.nc<1000:
                    if t>0:
                        print '{:>3}'.format(t),
                    else:
                        print ' '*3,                    
            print '\n'                

    def h(self, node):
        """Heuristic for the sliding puzzle: returns 0"""
        return 0
    ## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -



#______________________________________________________________________________
#

if __name__ == "__main__":

    #sp = Sliding_puzzle(nr=3, nc=8, N=15)
    sp = Sliding_puzzle()

    t0 = time.time()

    sol_ts = breadth_first_tree_search(sp)
    #sol_ts = breadth_first_tree_search(sp)

    #sol_ts = best_first_graph_search(sp, lambda node: node.path_cost) #done

    t1 = time.time()
    sp.print_solution(sol_ts)

    print "Solver took ",t1-t0, ' seconds'

