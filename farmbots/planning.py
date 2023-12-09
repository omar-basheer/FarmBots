from movement import drive_straight, spin
def neighboring_cells(curPos, map):   
    """
    Determines the neighbouring cells of the current position in the grid
        Params: 
            curPos: The current position of thr robot
            map: The grid map

        Return:
            A list of neighbouring cells to the current position
    """
    row = curPos[0]
    col = curPos[1]
    neighbours = []

    # U action results in (row-1, col)
    if (row-1 >= 0 and map[row-1][col] != 1):
        neighbours.append((row-1,col))

    # D action results in (row+1, col)
    if (row+1 < len(map) and map[row+1][col] != 1):
        neighbours.append((row+1,col))

    # R action results in (row, col+1)
    if (col+1 < len(map[0]) and map[row][col+1] != 1):
        neighbours.append((row,col+1))

    # L action results in (row, col-1)
    if (col-1 >= 0 and map[row][col-1] != 1):
        neighbours.append((row,col-1))

    return neighbours

def wavefront_alg(goalCell, map):
    """
    Creates a wavefront plan starting from the goalCell to every cell in the map.

    Params:
        goalCell: x,y coordinates of the goal coordinates
        map: World map
    """
    print("creating wavefront..." )
    frontier = []
    (x,y) = goalCell

    map[x][y] = 2
    frontier.append(goalCell)

    while frontier:
        node = frontier.pop(0)
        neighbours = neighboring_cells(node, map)

        for neighbour in neighbours:
            (a,b) = neighbour
            if map[a][b] == 0:
                map[a][b] = map[node[0]][node[1]] + 1
                frontier.append(neighbour)

    return map

def print_wavefront(wavefront_map):
    """
    Prints the wavefront map.

    Parameters:
    - wavefront_map: 2D list representing the wavefront map.
    """
    print("Wavefront Map:")
    for row in wavefront_map:
        print(row)
    print()

def trace_path(startCell, wavefrontPlan):
    """
    Traces a path from the start cell to the goal by picking the least neighbouring skill.

        Params:
            startCell: x, y coordinates of the starting cell
            wavefrontPlan: Completed wave front plan

        Return:
            Sequence of coordinattes to get from the start cell to the goal cell.
    """
    print("tracing path...")
    path = []

    while wavefrontPlan[startCell[0]][startCell[1]] != 2:
        neighbours = neighboring_cells(startCell, wavefrontPlan)

        minimum = neighbours[0]
        (a,b) = minimum
        lowest_value = wavefrontPlan[a][b]

        for neighbour in neighbours:
            (c,d) = neighbour
            if wavefrontPlan[c][d] < lowest_value:
                lowest_value = wavefrontPlan[c][d]
                minimum = neighbour
        path.append(minimum)
        startCell = minimum
    
    return path

def planPath(startCell, goalCell, map):
    """
    Plans a path for robot using the wavefront algorithm.

        @Params: 
            startCell: x,y coordinates of the start cell
            goalCell: x,y coordinates of the goal cell.

        @Return:
            Sequence of coordinattes to get from the start cell to the goal cell.

    """
    print("startCell:" + str(startCell) )
    print("goalCell:" + str(goalCell) )
    wavefrontPlan = wavefront_alg(goalCell, map)
    print_wavefront(wavefrontPlan)
    path = trace_path(startCell, wavefrontPlan)
    print("path:" + str(path))
    return path

directions = ['east','south','west','north']

def relDirection(pos1, pos2):
    """
    Computes the direction of pos2 relative to pos1, if pos2 is adjacent to pos1
        Params:
            pos1: x and y coordinates of current position of robot
            pos2: x and y coordinates of desired position of robot
        
        Return:
            Direction of pos2 relative to pos1. Direction is represented as an integer between 0 (corresponding to east) and
            3 (corresponding to north)
    """
    (x1, y1) = pos1
    (x2, y2) = pos2
    if x2==x1 and y2==y1+1:
        dir = 0
    elif x2==x1+1 and y2==y1:
        dir = 1
    elif x2==x1 and y2==y1-1:
        dir = 2
    elif x2==x1-1 and y2==y1:
        dir = 3
    else:
        raise ValueError(str(pos1)+" and " + str(pos2) + " are not neighbors,"\
                         +"so cannot compute relative direction between them.")
    
    return dir

def followPath(startCell, orientation, path):
    """Based on the start cell and orientation, this function allows the robot to
    follow the path from start to goal making the necessary turns and movements.

        Params:
            startCell: x,y coordinates of the start cell.
            orientation: direction of the robot.
            path: Path from start to goal.
    """
    curPos = startCell
    curDir = orientation
    print("following path...")

    for i in range(len(path)):
        nextPos = path[i]
        relDir = relDirection(curPos, nextPos)

        print("At pos " + str(curPos) + " facing direction " + str(curDir)
              + " (" + directions[curDir] + ")")
        
        print("Next pos is " + str(nextPos)
              + ", whose direction relative to the current pos is "
              + str(relDir) + " (" + directions[relDir] + ")")

        angle = relDir - curDir

        if angle == 1 or angle == -3:
            print('Turn right')
            spin("right", 90, 20)

        
        elif angle == -1 or angle == 3:
            print('Turn left')
            spin("left", 90, 20)
        
        elif angle == 2 or angle == -2:
            print("Turn around")
            spin("left", 180, 20)


        print("Go straight")
        drive_straight(45, 20)
        print()

        curPos = nextPos
        curDir = relDir

    print("curPos: " + str(curPos))
    print("curDir: " + str(curDir))
    return curPos, curDir


if __name__ == "__main__":
    print("main")
    # test_grid = [[0,0,0,0,0],
    #              [0,0,1,1,0],
    #              [0,0,1,0,0],
    #              [0,1,0,0,0]]
    
    # path = planPath((3,0), (3,4), test_grid)
    # followPath((3,0), 0, path)