from cab320_search import *

from cab320_sokoban import *

# define constant
FREE_SQUARE      = ' '
WALL_SQUARE      = '#'
BOX              = '$'
TARGET_SQUARE    = '.'
PLAYER           = '@'
PLAYER_ON_TARGET = '!'
BOX_ON_TARGET    = '*'
OBSTACLE = (WALL_SQUARE, BOX, BOX_ON_TARGET)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#                           UTILS
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def loadProblemFile(puzzleFileName):
    field = Warehouse()
    field.read_warehouse_file(puzzleFileName)
    visualized_by_line = field.visualize().split("\n")

    self.nr , self.nc = self.getProblemSize(visualized_by_line)
    problem = self.completeList(visualized_by_line, self.nc)
    return tuple(problem)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

class SokobanPuzzle(Problem):
    '''
    Class to represent a Sokoban puzzle.
    Your implementation should be compatible with the
    search functions of the module  cab320_search
    '''

##         "INSERT YOUR CODE HERE"
    
    # define class variables
    field = Warehouse()
    state_explored = ()
    n_nodes = 0

    def __init__(self, puzzleFileName):
        self.initial = self.loadProblemFile(puzzleFileName)
        self.goal = self.generateGoalState(self.initial)
        self.state_explored = (self.initial)       
        self.n_nodes = 0

    def getState(self):
        return list(self.current)

    def takeAction(self, action):
        print "takeAction(", action, ")"
        print "box in ", self.field.boxes
        print "worker in ", self.field.worker
        print "boxes in ", self.field.boxes
        print "targets in ", self.field.targets
        print "walls in ", self.field.walls
        return False

    '''
    Helper function:
    To load a given file and return relavant problem structure
    '''
    def loadProblemFile(self, puzzleFileName):
        self.field.read_warehouse_file(puzzleFileName)
        print self.field.visualize()
        return self.field.visualize().split("\n")

    '''
    Helper function:
    Find out the max no. of rows and columns to fix the size of the problem
    '''
    def getProblemSize(self, inList):
        n_cols = 0
        n_rows = 0
        for line in inList:
            n_rows += 1
            if len(line) > n_cols:
                n_cols = len(line)
        return n_rows, n_cols
    
    '''
    Helper function:
    To transform a complete/incomplete lines of data into a complete list of data
    so that [n * n_cols : n * n_cols + n_cols] is a complete line of data representing one row
    '''
    def completeList(self, inList, n_cols):
        completeList = []
        for line in inList:
            for i_col in range(n_cols):
                if line[i_col]:
                    completeList.append(line[i_col])
                else:
                    # extend the line if the given data is insufficient to complete a line
                    completeList.append(' ')
        return completeList

    '''
    Helper function:
    Generate the goal state from a given initial state
    '''
    def generateGoalState(self, initial):
        if initial:
            goallist = list(initial)
        else:
            goallist = list(self.initial)

        # transform all goal spots to goal box
        i_goalboxes = []
        searchlist = goallist
        i_goalspot = 0
        while '.' in searchlist:
            i_next_start = searchlist.index('.')
            i_goalspot += i_next_start
            i_goalboxes.append(i_goalspot)
            i_goalspot += 1
            searchlist = searchlist[i_next_start+1:]
        searchlist = list(self.initial)
        self.no_of_boxes = len(i_goalboxes)
        for i_goalbox in i_goalboxes:
            goallist[i_goalbox] = '*'

        # clear all normal boxes
        i_normalboxes = []
        searchlist = goallist
        i_box = 0
        while '$' in searchlist:
            i_next_start = searchlist.index('$')
            i_box += i_next_start
            i_normalboxes.append(i_box)
            i_box += 1
            searchlist = searchlist[i_next_start+1:]
        searchlist = list(self.initial)
        for i_box in i_normalboxes:
            goallist[i_box] = ' '

        # hidden the player
        if '@' in searchlist:
            i_player = searchlist.index('@')
        elif 'O' in searchlist:
            i_player = searchlist.index('O')
        goallist[i_player] = ' '
        return tuple(goallist)

        
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
               string returned by the method  WarehouseHowever.visualize()
    '''

##         "INSERT YOUR CODE HERE"

    # Load problem from file
    game = SokobanPuzzle(puzzleFileName)

    for action in actionSequence:
        if not game.takeAction(action):
            return "Failure"

    return game.getState


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

        raise NotImplementedError()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

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

        raise NotImplementedError()

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

