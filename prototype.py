# condition 1: all boxes should be placed on the goals
# condition 2: player cannot move out of the boundaries
# condition 3: player can only push a box
# condition 4: a box can be pushed only if the pushing direction is nothing
#               blocked
# condition 5: the next expanding node cannot be a state already explored
# condition 6: if there is multiple options to move a box, the shortest path
#               towards to nearest goal will be chosen
# condition 7: the player will attemp the closest box when game starts

# flow:
# 1. player try to find the closest box that is not yet in a goal
#    and not yet tried
# 2. player find the shortest path to reach the box
# 3. when reach the box:
#       4. player try to find the shortest path to move the box to the
#          nearnest goal
#           5. if there is a path:
#               6. search from the explored states for the next step,
#                  if no match:
#                   7. move to the appropriate edge and push the box
#                      and repeat 3
#               8. if the state is already explored, repeat 4
#           9. if the box can not move in current direction, player try to
#              find another possible edge, if found, repeat 3
#       10. if no other way to push the box, repeat 1






















def expandNode(state):
    # given a state, expand the possible move of the player

    # direction = {left, right, down, left}
    # if direction->next != wall



def shortestPath(state, player, box):
    # given a state, the location of the player, and the target box,
    # the function will return the shortest path form the player to the box


def isExplored(state):
    # give a state, the function will check if it is an explolred state
    

def moveToBox(state):




