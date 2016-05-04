from cab320_search import *

from cab320_sokoban import *

from multiprocessing import Process, Queue
import time

# define constant
FREE_SQUARE      = ' '
WALL_SQUARE      = '#'
BOX              = '$'
TARGET_SQUARE    = '.'
PLAYER           = '@'
PLAYER_ON_TARGET = '!'
BOX_ON_TARGET    = '*'
TABOO_SQUARE     = 'X'

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

class SokobanPuzzle(Problem):
    '''
    Class to represent a Sokoban puzzle.
    Your implementation should be compatible with the
    search functions of the module  cab320_search
    '''

##         "INSERT YOUR CODE HERE"

    def __init__(self, puzzleFileName):
        self.initial = self.loadProblemFile(puzzleFileName)
        self.current_state = self.initial
        self.state_explored = (self.initial)
        self.node_count = 0

    def getState(self, state=None):
        if state == None:
            state = self.current_state
        return state.visualize()

    def takeAction(self, action, state=None):
        if not state:
            state = self.current_state
        if (action == "Up"):
            return self.__moveUp__(state)
        if (action == "Down"):
            return self.__moveDown__(state)
        if (action == "Left"):
            return self.__moveLeft__(state)
        if (action == "Right"):
            return self.__moveRight__(state)
        return False

    '''
    A method to move the player
    '''
    def __move__(self, state, playerNextLoc, boxNextLoc):
        # check if the player movement violates any constraint
        if playerNextLoc in state.walls:
            # player movement cannot be blocked by a wall
            return False
        elif playerNextLoc in state.boxes:
            # player attemps to push a box
            if boxNextLoc in state.walls + state.boxes + self.findTaboos(state):
                # player moving box cannot be blocked by a wall or another box
                return False

        # if satisfied the constraints, do the move

        if playerNextLoc in state.boxes:
            # push the box above the player
            new_boxes_location = []
            for box in state.boxes:
                if box == playerNextLoc:
                    new_boxes_location.append(boxNextLoc)
                else:
                    new_boxes_location.append(box)
            state.boxes = new_boxes_location

            state.worker = playerNextLoc
        else:
            # player move freely
            state.worker = playerNextLoc  
        return True


    '''
    A method to move the player up
    '''
    def __moveUp__(self, state=None):
        current_x, current_y = state.worker
        positionAbovePlayer = (current_x, current_y - 1)
        positionAbovePlayerAndBox = (current_x, current_y - 2)
        return self.__move__(state, positionAbovePlayer, positionAbovePlayerAndBox)

    '''
    A method to move the player down
    '''
    def __moveDown__(self, state=None):
        current_x, current_y = state.worker
        positionBelowPlayer = (current_x, current_y + 1)
        positionBelowPlayerAndBox = (current_x, current_y + 2)
        return self.__move__(state, positionBelowPlayer, positionBelowPlayerAndBox)

    '''
    A method to move the player left
    '''
    def __moveLeft__(self, state=None):
        current_x, current_y = state.worker
        positionPlayerLeft = (current_x - 1, current_y )
        positionPlayerAndBoxLeft = (current_x - 2, current_y)
        return self.__move__(state, positionPlayerLeft, positionPlayerAndBoxLeft)

    '''
    A method to move the player right
    '''
    def __moveRight__(self, state=None):
        current_x, current_y = state.worker
        positionPlayerRight = (current_x + 1, current_y )
        positionPlayerAndBoxRight = (current_x + 2, current_y)
        return self.__move__(state, positionPlayerRight, positionPlayerAndBoxRight)

    def actions(self, state=None):
        validActions = ("Up", "Down", "Left", "Right")
        L = []
        if not state:
            state = self.current_state

        for action in validActions:
            trystate = state.copy()
            if self.takeAction(action, trystate):
                L.append(action)
        return L

    def result(self, state, action):
        next_state = state.copy()
        currentTime = time.time()
        if self.takeAction(action, next_state):
            self.node_count += 1
            if self.node_count > 0 and self.node_count % 500 == 0:
                print "Nodes reachs ", self.node_count
            return next_state
        else:
            return ()

    '''
    A method to show the taboo cells as marked 'X'
    '''
    def findTaboos(self, state=None):
        if not state:
            state = self.current_state
        tabooState = state.copy()

        # find all dead corner
        freeSpaces = findPositionIterator(list(tabooState.visualize().split('\n')), ' ')
        taboos = []
        for space in freeSpaces:
            current_x, current_y = space
            north_x, north_y = current_x, current_y - 1
            south_x, south_y = current_x, current_y + 1
            east_x, east_y = current_x + 1, current_y
            west_x, west_y = current_x - 1, current_y
            if ((north_x, north_y) in tabooState.walls and (east_x, east_y) in tabooState.walls)\
                or \
                ((south_x, south_y) in tabooState.walls and (east_x, east_y) in tabooState.walls)\
                or \
                ((south_x, south_y) in tabooState.walls and (west_x, west_y) in tabooState.walls)\
                or \
                ((north_x, north_y) in tabooState.walls and (west_x, west_y) in tabooState.walls):
                taboos.append(space)

        # generate a 2 dimensions list of the current state
        visualizeLine = list(tabooState.visualize().split('\n'))
        vis = []
        n_col = 0
        n_row = 0
        for line in visualizeLine:
            n_row += 1
            linelist = list(line)
            if len(linelist) > n_col:
                n_col = len(linelist)
            vis.append(linelist)
        self.nc = n_col
        self.nr = n_row

        # find edge of wall that don't have a goal square
        for row in range(n_row):
            if TARGET_SQUARE not in vis[row] and BOX_ON_TARGET not in vis[row]:
                if WALL_SQUARE in vis[row]:
                    walls_in_line = list(findIterator(''.join(vis[row]), WALL_SQUARE))
                    for i in range(len(walls_in_line)-1):
                        if abs(walls_in_line[i] - walls_in_line[i+1]) > 1:
                            if row > 0:
                                bounded_with_walls = True;
                                for j in range(walls_in_line[i] + 1, walls_in_line[i+1]):
                                    if (vis[row-1][j] != WALL_SQUARE):
                                        bounded_with_walls = False
                                if bounded_with_walls:
                                    for j in range(walls_in_line[i] + 1, walls_in_line[i+1]):
                                        if (j,row) not in taboos:
                                            taboos.append((j,row))
                            if row < n_row - 1:
                                bounded_with_walls = True;
                                for j in range(walls_in_line[i] + 1, walls_in_line[i+1]):
                                    if (vis[row+1][j] != WALL_SQUARE):
                                        bounded_with_walls = False
                                if bounded_with_walls:
                                    for j in range(walls_in_line[i] + 1, walls_in_line[i+1]):
                                        if (j,row) not in taboos:
                                            taboos.append((j,row))
        for col in range(n_col):
            col_line = []
            for row in range(n_row):
                col_line.append(vis[row][col])
            if TARGET_SQUARE not in col_line and BOX_ON_TARGET not in col_line:
                if WALL_SQUARE in col_line:
                    walls_in_line = list(findIterator(''.join(col_line), WALL_SQUARE))
                    for i in range(len(walls_in_line)-1):
                        if abs(walls_in_line[i] - walls_in_line[i+1]) > 1:
                            if col > 0:
                                bounded_with_walls = True;
                                for j in range(walls_in_line[i] + 1, walls_in_line[i+1]):
                                    if (vis[j][col-1] != WALL_SQUARE):
                                        bounded_with_walls = False
                                if bounded_with_walls:
                                    for j in range(walls_in_line[i] + 1, walls_in_line[i+1]):
                                        taboos.append((col,j));
                            if col < n_col - 1:
                                bounded_with_walls = True;
                                for j in range(walls_in_line[i] + 1, walls_in_line[i+1]):
                                    if (vis[j][col+1] != WALL_SQUARE):
                                        bounded_with_walls = False
                                if bounded_with_walls:
                                    for j in range(walls_in_line[i] + 1, walls_in_line[i+1]):
                                        taboos.append((col,j));

        return taboos

    def showTabooCells(self, state=None):
        if not state:
            state = self.current_state

        # generate a 2 dimensions list of the current state
        visualizeLine = list(state.visualize().split('\n'))
        vis = []
        n_col = 0
        n_row = 0
        for line in visualizeLine:
            n_row += 1
            linelist = list(line)
            if len(linelist) > n_col:
                n_col = len(linelist)
            vis.append(linelist)

        for taboo in self.findTaboos(state):
            col, row = taboo
            vis[row][col] = 'X'

        return '\n'.join([''.join(line) for line in vis])

    '''
    A method to check if each location of the box in the given state is a target spot
    '''
    def goal_test(self, state):
        for box_loc in state.boxes:
            if not box_loc in state.targets:
                return False
        return True
    
    def print_solution(self, goal_node):
        """
            Shows solution represented by a specific goal node.
            For example, goal node could be obtained by calling 
                goal_node = breadth_first_tree_search(problem)
        """
        # path is list of nodes from initial state (root of the tree)
        # to the goal_node
        path = goal_node.path()
        # print the solutiona
        print "Solution takes {0} steps from the initial state\n".format(len(path)-1)
        self.print_state(path[0].state)
        print "to the goal state\n"
        self.print_state(path[-1].state)
        print "Total ", self.node_count, " nodes was generated.\n"
        print "Below is the sequence of moves\n"
        for node in path:
            self.print_node(node)

    def print_node(self, node):
        """Print the action and resulting state"""
        if node.action:
            print "Move "+node.action
        self.print_state(node.state)

    def print_state(self, s):
         print s.visualize()

    def getSolution(self, goal_node):
        path = goal_node.path()
        actionSequence = []
        for node in path[1:]:
            actionSequence.append(node.action)
        return actionSequence


    def h(self, node):
        """Heuristic for the sliding puzzle: returns 0"""
        return 0

    '''
    Helper function:
    To load a given file and return relavant problem structure
    '''
    def loadProblemFile(self, puzzleFileName):
        field = Warehouse()
        field.read_warehouse_file(puzzleFileName)
        return field
        
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def checkActions(puzzleFileName, actionSequence):
    '''
    This is a function called by the automatic marker.

    Your implementation should load a Sokoban puzzle from a text file,
    then try to apply the sequence of actions listed in actionSequence.

    @param puzzleFileName: file name of the puzzle
         (same format as for the files in the warehouses directory)
    @param actionSequence: a sequence of actions.
           For example, ['Left', 'Down', 'Down','Right', 'Up', 'Down']
    @return:
        The string 'Failure', if one of the move was not successul.
           For example, if the agent tries to push two boxes,
                        or push into to push into a wall.
        Otherwise, if all moves were successful return                 
               A string representing the state of the puzzle after applying
               the sequence of actions.  This should be the same string as the
               string returned by the method Warehouse.visualize()
    '''

##         "INSERT YOUR CODE HERE"

    # Load problem from file
    game = SokobanPuzzle(puzzleFileName)
    testState = game.initial.copy()
    for action in actionSequence:
        if not game.takeAction(action, testState):
            return "Failure"
        else:
            game.current_state = testState

    return game.getState()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def tabooCells(puzzleFileName):
    '''
    This is a function called by the automatic marker.

    Your implementation should load a Sokoban puzzle from a text file,
    then identify the cells that should be avoided in the sense that if
    a box get pushed on such a cell then the puzzle becomes unsolvable.

    @param puzzleFileName: file name of the puzzle
         (same format as for the files in the warehouses directory)
    @return:
               A string representing the puzzle with the taboo cells marked with an 'X'.
               Apart from the 'X's, the string should follows the same format as the
               string returned by the method  Warehouse.visualize()
    '''

##         "INSERT YOUR CODE HERE"
    game = SokobanPuzzle(puzzleFileName)
    return game.showTabooCells()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_sokoban(puzzleFileName, return_queue):
    trace_list = []
    game = SokobanPuzzle(puzzleFileName)
    t0 = time.time()
    sol_ts = astar_search(game)
    if sol_ts == None:
        movement = ['Impossible']
        return_queue.put([movement,""])
        return
    t1 = time.time()
    movement = game.getSolution(sol_ts)
    goal_node = sol_ts.path()

    trace_list.append("Boxes = " + str(len(goal_node[0].state.boxes)))
    trace_list.append("Nodes generated = " + str(game.node_count))
    trace_list.append("Time used = " + str(t1-t0))
    trace_list.append("Movement needed = " + str(len(movement)))
    if (t1-t0) >0:
        return_queue.put([movement,'\n'.join(trace_list)])
    else:
        return_queue.put([["Skipped"],""])
    return

def solveSokoban_elementary(puzzleFileName, timeLimit = None):
    '''
    This is a function called by the automatic marker.

    This function should solve the puzzle defined in a file.

    @param puzzleFileName: file name of the puzzle
         (same format as for the files in the warehouses directory)
    @param time_limit: The time limit for this agent in seconds .
    @return:
        A list of strings.
        If timeout return  ['Timeout']
        If puzzle cannot be solved return ['Impossible']
        If a solution was found, return a list of elementary actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
    '''

##         "INSERT YOUR CODE HERE"
    if timeLimit != None:
        print "Attemp to solve this problem within ", timeLimit, ' seconds.'
        result_queue = Queue()
        p = Process(target=solve_sokoban, args=(puzzleFileName,result_queue))
        p.start()
        p.join(timeLimit)
        if p.is_alive():
            # Terminate
            p.terminate()
            p.join()
            return ['Timeout']
        resultset = result_queue.get()
        print resultset[1]
        return resultset[0]
    else:
        return solve_sokoban(puzzleFileName)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solveSokoban_macro(puzzleFileName, timeLimit = None):
        '''
        This is a function called by the automatic marker.
        
        This function has the same purpose as 'solveSokoban_elementary', but 
        it should internally use macro actions as suggested 
        in the assignment description. Although it internally uses macro 
        actions, this function should return a sequence of 
        elementary  actions.


        @param puzzleFileName: file name of the puzzle
             (same format as for the files in the warehouses directory)
        @param time_limit: The time limit for this agent in seconds .
        @return:
            A list of strings.
            If timeout return  ['Timeout']
            If puzzle cannot be solved return ['Impossible']
            If a solution was found, return a list elementary actions that solves
                the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
                For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
                If the puzzle is already in a goal state, simply return []
        '''

##         "INSERT YOUR CODE HERE"

        raise NotImplementedError()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

