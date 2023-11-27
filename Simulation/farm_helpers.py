#!/usr/bin/env pybricks-micropython

GRID_SIZE = 12

def initialize_farm_space(fruit_map, grid_size=GRID_SIZE):
    # Initialize a grid with all cells initially empty
    world_grid = [['empty' for _ in range(grid_size)] for _ in range(grid_size)]

    # Place fruits in the grid based on the provided fruit map
    for fruit_location, fruit_color in fruit_map.items():
        row, col = fruit_location
        # Check if the provided location is within the grid boundaries
        if 0 <= row < grid_size and 0 <= col < grid_size:
            world_grid[row][col] = f'fruit_{fruit_color}'

    return world_grid

def update_farm_space(farm_space, robot_position):
    x, y = robot_position['x'], robot_position['y']

    # Update the farm_space matrix based on the robot's position
    if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
        farm_space[int(x)][int(y)] = 'Occupied'

