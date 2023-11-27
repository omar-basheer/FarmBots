from part_one import find_four_neighbors
def wavefrontAlg(goal, grid_map):
    print('starting wavefront')
    queue = [goal]
    explored = []  # to keep track of visited nodes to a void cycles
    while queue:
        curr = queue.pop(0)
        currValue = grid_map[curr[0]][curr[1]]
        explored.append(curr)
        neighbours = find_four_neighbors(currPos=curr, grid_map=grid_map)
        for neighbour in neighbours:
            if neighbour not in explored:
                grid_map[neighbour[0]][neighbour[1]] = currValue+ 1
                queue.append(neighbour)
                print(grid_map)
    return grid_map


gridMap = [[0,0,0,0,0], [0,0,1,1,0], [0,0,1,0,0], [0,1,0,0,2]]
print( wavefrontAlg((3,4), grid_map=gridMap))