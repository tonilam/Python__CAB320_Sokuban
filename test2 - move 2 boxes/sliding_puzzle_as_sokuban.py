
##    Last modified 2015-03-08
##    by f.maire@qut.edu.au

                     
#from cab320_search_SOLUTION import *  # Search module adapted from AIMA for CAB320
from cab320_search import *  # Search module adapted from AIMA for CAB320
import random
import time
import re

# An on-line applet for the sliding puzzle   http://mypuzzle.org/sliding

class Sliding_puzzle(Problem):
    """
    The tiles are in a a grid with self.nr rows and self.nc columns.
    The tiles are read row by row.
    The actions are 'U','D','L' and 'R'  (move the blank tile up, down, left  right)
    """
    OBSTACLE = ('#','*','$')
    PLAYER = '@'
    PLAYER_ON_GOAL = 'O'
    state_explored = ()
    step_inspected = 0 

    def actions(self, state):
        # index of the player in a give state
        if self.PLAYER in state:
            i_player = state.index(self.PLAYER)
        elif self.PLAYER_ON_GOAL in state:
            i_player = state.index(self.PLAYER_ON_GOAL)
        else:
            return []
        n_box = 0
        i_boxes = ()
        i_boxes_in_goal = ()
        i_box = -1
        i = 0
        while ('$' in state[i:]):
            i_box = i + state[i:].index('$')
            if (i_box >= 0):
                i_boxes = i_boxes + (i_box,)
                i = i_box + 1
                n_box += 1
                
        i = 0
        while ('*' in state[i:]):
            i_box = i + state[i:].index('*')
            if (i_box >= 0):
                i_boxes_in_goal = i_boxes_in_goal + (i_box,)
                i = i_box + 1
                n_box += 1
            
        L = []  # list of legal actions
        free_box_found = n_box > 0
        # UP: If the there is not a wall 1 row above the player, or
        #     there is a box somewhere and the box is 1 row above the playe and there is not a wall 1 row above the box
        player_bounded_above = state[i_player - self.nc] == '#'
        box_above_player = (i_player - self.nc) in (i_boxes + i_boxes_in_goal)
        if box_above_player: 
            play_and_box_bounded_above = state[i_player - self.nc*2] in self.OBSTACLE
        if (not free_box_found and not player_bounded_above) or\
           (free_box_found and not box_above_player and not player_bounded_above) or\
           (free_box_found and box_above_player and not play_and_box_bounded_above):
            L.append('U')
        # DOWN: If the there is not a wall 1 row below the player, or
        #       there is a box somewhere and the box is 1 row below the playe and there is not a wall 1 row below the box
        player_bounded_below = state[i_player + self.nc] == '#'
        box_below_player = (i_player + self.nc) in (i_boxes + i_boxes_in_goal)
        if box_below_player:
            play_and_box_bounded_below = state[i_player + self.nc*2] in self.OBSTACLE
        if (not free_box_found and not player_bounded_below) or\
           (free_box_found and not box_below_player and not player_bounded_below) or\
           (free_box_found and box_below_player and not play_and_box_bounded_below):
            L.append('D')
        # LEFT: if the there is not a wall 1 column left from the player, or
        #       there is a box somewhere and the box is 1 column left from the playe and there is not a wall 1 column left from the box
        player_bounded_left = state[i_player - 1] == '#'
        box_leftto_player = (i_player - 1) in (i_boxes + i_boxes_in_goal)
        if box_leftto_player:
            play_and_box_bounded_left = state[i_player - 1*2] in self.OBSTACLE

##        print "i_player = ", i_player
##        print "all boxes = ", i_boxes + i_boxes_in_goal
##        print "player_bounded_left", player_bounded_left
##        print "box_leftto_player", box_leftto_player
##        if box_leftto_player:
##            print "play_and_box_bounded_left", play_and_box_bounded_left
            
        if (not free_box_found and not player_bounded_left) or\
           (free_box_found and not box_leftto_player and not player_bounded_left) or\
           (free_box_found and box_leftto_player and not play_and_box_bounded_left):
            L.append('L')
        # RIGHT: Iif the there is not a wall 1 column right from the player, or
        #        there is a box somewhere and the box is 1 column right from the playe and there is not a wall 1 column right from the box
        player_bounded_right = state[i_player + 1] == '#'
        box_rightto_player = (i_player + 1) in (i_boxes + i_boxes_in_goal)
        if box_rightto_player:
            play_and_box_bounded_right = state[i_player + 1*2] in self.OBSTACLE

##        print "i_boxes = ", i_boxes
##        print "i_boxes_in_goal = ", i_boxes_in_goal
##        print "player_bounded_right", player_bounded_right
##        print "box_rightto_player", box_rightto_player
##        if box_rightto_player:
##            print "play_and_box_bounded_right", play_and_box_bounded_right
        
        if (not free_box_found and not player_bounded_right) or\
           (free_box_found and not box_rightto_player and not player_bounded_right) or\
           (free_box_found and box_rightto_player and not play_and_box_bounded_right):
            L.append('R')

##        print "Possible move: ", L
        return L
    
    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal, as specified in the constructor. Override this
        method if checking against a single self.goal is not enough."""
        checkstate = list(state);
        if '@' in state:
            i_player = state.index('@')
        elif 'O' in state:
            i_player = state.index('O')
        else:
            return False
        checkstate[i_player] = ' ';
        return tuple(checkstate) == self.goal
    
    def result(self, state, action):
        """
        Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state).
        """
        # index of the blank
##        next_state = state[:] # Note that  next_state=state   would simply create an alias
        next_state = list(state)
        if '@' in state:
            i_player = state.index('@')
        elif 'O' in state:
            i_player = state.index('O')
        i_box = -1
        #assert action in self.actions(state)  # defensive programming!
        # UP: if blank not on top row, swap it with tile above it
        if action == 'U':
            i_swap = i_player - self.nc
            if next_state[i_swap] in ('$','*'):
                i_box = i_swap - self.nc
        # DOWN: If blank not on bottom row, swap it with tile below it
        if action == 'D':
            i_swap = i_player + self.nc
            if next_state[i_swap] in ('$','*'):
                i_box = i_swap + self.nc
        # LEFT: If blank not in left column, swap it with tile to the left
        if action == 'L':
            i_swap = i_player - 1
            if next_state[i_swap] in ('$','*'):
                i_box = i_swap - 1
        # RIGHT: If blank not on right column, swap it with tile to the right
        if action == 'R':
            i_swap = i_player + 1
            if next_state[i_swap] in ('$','*'):
                i_box = i_swap + 1


        clear_zone = ' '
        goals_spot = '.'
        player_as_normal = '@'
        player_on_goal = 'O'
        box_as_normal = '$'
        box_on_goal = '*'
        player_move_a_goal_box = next_state[i_swap] == '*'
        if i_box >= 0:
            dest_of_box_is_a_goal = next_state[i_box] == '.'
        else:
            dest_of_box_is_a_goal = False
        if (state[i_player] == player_as_normal):
            if (i_box >= 0 and i_box < self.nc * self.nr):
                # if a box move is under process
                if (player_move_a_goal_box):
                    # moving a goal box away from the goal, and player step on the goal
                    if (dest_of_box_is_a_goal):
                        next_state[i_player], next_state[i_swap], next_state[i_box] = clear_zone, player_on_goal, '*'
                    else:
                        next_state[i_player], next_state[i_swap], next_state[i_box] = clear_zone, player_on_goal, '$'
                elif (next_state[i_box] == '.'):
                    # moving a box towards the goal
                    next_state[i_player], next_state[i_swap], next_state[i_box] = clear_zone, '@', '*'
                else:
                    # moving a box to a clear zone
                    next_state[i_player], next_state[i_swap], next_state[i_box] = clear_zone, '@', '$'
            else:
                # player move freely
                if (next_state[i_swap] == '.'):
                    next_state[i_swap], next_state[i_player] = 'O', clear_zone
                else:
                    next_state[i_swap], next_state[i_player] = '@', clear_zone
        elif (state[i_player] == player_on_goal):
            org_player_space = goals_spot
            current_player_position = i_player
            next_player_position = i_swap
            if (i_box >= 0 and i_box < self.nc * self.nr):
                if (player_move_a_goal_box):
                    if (dest_of_box_is_a_goal):
                        next_state[i_player], next_state[i_swap], next_state[i_box] = org_player_space, player_on_goal, box_on_goal
                    else:
                        next_state[i_player], next_state[i_swap], next_state[i_box] = org_player_space, player_on_goal, box_as_normal
                elif (dest_of_box_is_a_goal):
                    next_state[i_player], next_state[i_swap], next_state[i_box] = org_player_space, player_as_normal, box_on_goal
                else:
                    next_state[i_player], next_state[i_swap], next_state[i_box] = org_player_space, player_as_normal, box_as_normal
            else:
                if (next_state[next_player_position] == '.'):
                    next_state[next_player_position], next_state[current_player_position] = player_on_goal, org_player_space
                else:
                    next_state[next_player_position], next_state[current_player_position] = player_as_normal, org_player_space

        if (self.step_inspected % 1000 == 0):
            print "Inspecting node #", self.step_inspected, " - #", self.step_inspected + 999
        if (next_state not in self.state_explored):
            self.state_explored = self.state_explored + (next_state,)
            #if self.step_inspected > 1030:
            self.step_inspected += 1
##            print "Adds node #", self.step_inspected, ", ", action
##            self.print_state(next_state)
            return tuple(next_state) # use tuple to make the state hashable
        else:
##            print "Node duplicated, skip ", action
            return ()
    
    def __init__(self,
                 nr = 7, # number of rows
                 nc = 6, # number of columns
                 goal = None, # goal state 
                 initial = None, # initial state
                 N = 100 # number of random moves from goal state
                        # if no initial state given
                 ): 
        # Problem.__init__(self, initial, goal)
        self.nr , self.nc = nr , nc
        if goal:
            self.goal = goal
        else:
            self.goal = ('#', '#', '#', '#', ' ', ' ',
                         '#', ' ', '*', '#', ' ', ' ',
                         '#', ' ', ' ', '#', '#', '#',
                         '#', '*', ' ', ' ', ' ', '#',
                         '#', ' ', ' ', ' ', ' ', '#',
                         '#', ' ', ' ', '#', '#', '#',
                         '#', '#', '#', '#', ' ', ' ')            
        if initial:
            self.initial = initial
        else:
            self.initial = ('#', '#', '#', '#', ' ', ' ',
                            '#', ' ', '.', '#', ' ', ' ',
                            '#', ' ', ' ', '#', '#', '#',
                            '#', '*', '@', ' ', ' ', '#',
                            '#', ' ', ' ', '$', ' ', '#',
                            '#', ' ', ' ', '#', '#', '#',
                            '#', '#', '#', '#', ' ', ' ')            
        self.state_explored = self.state_explored + (list(self.initial),)
        self.initial = tuple(self.initial)
        self.goal = tuple(self.goal)        
        step_inspected = 0

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

    sp = Sliding_puzzle(nr=7, nc=6, N=1000)

    t0 = time.time()
    sol_ts = breadth_first_search(sp)
    t1 = time.time()
    sp.print_solution(sol_ts)
    print "breadth_first_tree_search took ",t1-t0, ' seconds'
##
##    sol_ts = breadth_first_search_v0(sp)
##    t1 = time.time()
##    #sp.print_solution(sol_ts)
##    print "breadth_first_search_v0 took ",t1-t0, ' seconds'
##
##    sol_ts = breadth_first_search(sp)
##    t1 = time.time()
##    #sp.print_solution(sol_ts)
##    print "breadth_first_search took ",t1-t0, ' seconds'
##
##    sol_ts = uniform_cost_search(sp)
##    t1 = time.time()
##    #sp.print_solution(sol_ts)
##    print "uniform_cost_search took ",t1-t0, ' seconds'
##
##    sol_ts = depth_limited_search(sp)
##    t1 = time.time()
##    #sp.print_solution(sol_ts)
##    print "depth_limited_search took ",t1-t0, ' seconds'
##
##    sol_ts = iterative_deepening_search(sp)
##    t1 = time.time()
##    #sp.print_solution(sol_ts)
##    print "iterative_deepening_search took ",t1-t0, ' seconds'
##
##    sol_ts = astar_search(sp)
##    t1 = time.time()
##    #sp.print_solution(sol_ts)
##    print "astar_search took ",t1-t0, ' seconds'
