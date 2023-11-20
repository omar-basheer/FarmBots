#!/usr/bin/env pybricks-micropython

GRID_SIZE = 5

def initialize_farm_space():
    return [['Empty' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

def update_farm_space(farm_space, robot_position):
    x, y = robot_position['x'], robot_position['y']

    # Update the farm_space matrix based on the robot's position
    if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
        farm_space[int(x)][int(y)] = 'Occupied'