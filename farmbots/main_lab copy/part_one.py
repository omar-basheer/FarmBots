
def find_four_neighbors(currPos, grid_map):
    """
    Finds the four neighbours of the given position in the grid map.

    Args:
        currPos: The current position as a tuple of (row, col).
        grid_map: The grid map as a 2D array.

    Returns:
        A list of the four neighbours as tuples of (row, col).
    """
    neighbours = []
    row = len(grid_map)
    col = len(grid_map[0])

    #row down
    if currPos[0] + 1 < row and grid_map[currPos[0] + 1][ currPos[1]] != 1 :
        neighbours.append((currPos[0] + 1, currPos[1]))
    #row up
    if currPos[0] - 1 >=  0 and grid_map[currPos[0] - 1] [currPos[1]] != 1 :
        neighbours.append((currPos[0] - 1, currPos[1]))
    #col right
    if currPos[1] + 1 < col and grid_map[currPos[0]] [currPos[1] +1 ] != 1 :
        neighbours.append((currPos[0], currPos[1] + 1))
    #col left
    if currPos[1] - 1 >= 0 and grid_map[currPos[0]] [currPos[1]-1] != 1:
        neighbours.append((currPos[0], currPos[1] - 1))
    
    return neighbours


def findPath(currPos, wavefront):
    """
    Finds the shortest path from the start position to the end position in the wavefront.

    Args:
        currPos: The current position as a tuple of (row, col).
        wavefront: The wavefront as a 2D array.

    Returns:
        A list of the positions in the shortest path.
    """
    path = []
    while wavefront[currPos[0]][currPos[1]] != 2:
        neighbours = find_four_neighbors(currPos=currPos, grid_map= wavefront)
        minValueTuple = neighbours[0]
        minValue = wavefront[minValueTuple[0]][minValueTuple[1]]
        for neighbour in neighbours:
            if wavefront[neighbour[0]][neighbour[1]]< minValue:
                minValue = wavefront[neighbour[0]][neighbour[1]]
                minValueTuple = neighbour
        path.append(minValueTuple)
        currPos = minValueTuple
    return path
