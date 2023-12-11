#!/usr/bin/env pybricks-micropython
import random
import time
from comms import close_bluetooth_connection, create_mailbox, decode_message, send_server_update_message, start_bluetooth_server, test_handshake, connect_to_bluetooth_server
from farm_helpers import initialize_client_world
from planning import followPath, planPath
from localization import get_current_position
from pybricks import ev3brick as brick


curr_x, curr_y, curr_orientation = 0, 0, 0

def print_world(farm_space):
    for row in farm_space:
        print(" ".join(map(str, row)))

def set_current_position(x, y, orientation):
    curr_x, curr_y, curr_orientation = x, y, orientation

def get_current_position():
    return curr_x, curr_y, curr_orientation

def obstacleDetected():
    return False

def pickup_fruit(current_position, goal_position, world):
    print("planning path from current position to goal...")
    global curr_x, curr_y, curr_orientation 
    x, y, orientation = current_position
    curr_path = planPath((x, y), goal_position, world)
    print("planned path" + str(curr_path))

    for next_position in curr_path:
        print("checking for obstacles...")
        if obstacleDetected():
            print("waiting for client to pass...")
            while obstacleDetected():
                pass
        print("moving to next position: ", next_position)
        new_position, new_orientation = followPath((x, y), orientation,[next_position])
        x, y = new_position
        orientation = new_orientation
        print("current position:" + str(new_position))
        print("last position in path:" + str(curr_path[-1]))

        if new_position == curr_path[-1]:
            curr_x, curr_y, curr_orientation = x, y, orientation  
            return True, x, y, orientation
    return False, x, y, orientation

# def pickup_fruit(current_position, goal_position, world):
#     print("planning path from current position to goal...")
#     x, y, orientation = current_position
#     curr_path = planPath((x,y), goal_position, world)
#     print("planned path" + str(curr_path))

#     followPath((x,y), orientation, curr_path)
#     final_position = get_current_position()
#     print("final position:" + final_position)
#     print("last position in path:" + curr_path[-1])

#     if final_position == curr_path[-1]:
#         return True
#     return False

def main():
    GRID_SIZE = 5
    server_brick_address = 'ash-ev3-07'
    client_mailbox_name = 'client1'
    # x, y, orientation = 0, 0, 0
    
    # step 1: connect to server
    print("starting bluetooth client...")
    client = connect_to_bluetooth_server(server_brick_address)

    print("receiving bluetooth handshake...")
    client_mailbox = create_mailbox(client_mailbox_name, client)
    print("connected")

    # step 2: initialize world for client
    farm_space = initialize_client_world(grid_size=GRID_SIZE)
    print_world(farm_space)

    # step 3: set iniital client state:
    client_status = 'free'
    task_state = None
    # position = get_current_position()
    position = curr_x, curr_y, curr_orientation
    fruit_location = None

    # step3.1: while connection to server is open
    while client:
        # step 3.1.1: send update message to server
        print("updating server with current status...")
        send_server_update_message(client_mailbox, client_mailbox_name, client_status, task_state, position, fruit_location)
        print("server updated !")

        # step 3.1.2: wait for response to message from server
        print("receiving task message from server...")
        encoded_task_message = client_mailbox.read()
        print("task received!")
        task_message = decode_message(encoded_task_message)
        if task_message:
             # step 3.1.3.1: update client state:
            client_status = 'busy'
            task_state = 'in progress'
            position = position
            fruit_location = task_message
            print("current position: " + str(position))
            print("Mission: collect fruit at: " +str(fruit_location))
            brick.display.text(task_message)

            # step 3.1.3.2: execute path planning and fruit collecting
            print("executing task...")
            task_success, x, y, orientation = pickup_fruit(position, fruit_location, farm_space)
            set_current_position(x, y, orientation)
            farm_space = initialize_client_world(grid_size=GRID_SIZE)

            if task_success == True:
                # update client information
                client_status = 'free'
                task_state = 'completed'
                position = get_current_position()
                fruit_location = task_message
            else:
                # update client information
                client_status = 'busy'
                task_state = 'in progress'
                position = get_current_position()
                fruit_location = task_message
              

if __name__ == "__main__":
   main()



