#!/usr/bin/env pybricks-micropython
from communication import connect_to_bluetooth_server, create_mailbox, decode_message, send_initial_client_position
from farm import initialize_client_world
from movement import close_gripper, open_gripper
from planning import followPath, planPath
from server import print_world
# from pybricks import ev3brick as brick

def obstacleDetected():
    return False

def pickup_fruit(current_position, goal_position, world):
    print("planning path from current position to goal...")
    x, y, orientation = current_position
    curr_path = planPath((x, y), goal_position, world)
    print("planned path" + str(curr_path))
    
    open_gripper()
    followPath((x, y), orientation,curr_path)
    close_gripper()
    # print("current position:" + str(new_position))
    # print("last position in path:" + str(curr_path[-1]))

    return True


def pickup_fruit_and_return(current_position, goal_position, start_position, world):
    print("Planning path from current position to goal...")
    x, y, orientation = current_position

    # Plan path to the fruit
    path_to_fruit = planPath((x, y), goal_position, world)
    print("Planned path to the fruit: " + str(path_to_fruit))

    # Follow path to the fruit
    open_gripper()
    followPath((x, y), orientation,path_to_fruit)
    close_gripper()

    # Plan path back to the start position
    farm_space = initialize_client_world(grid_size=5)
    nx, ny  = path_to_fruit[-1]
    print (str((nx,ny)))
    path_to_start = planPath((nx, ny), (start_position[0], start_position[1]), farm_space)
    print("Planned path back to start position: " + str(path_to_start))
        
    followPath((nx, ny), orientation, path_to_start)

    return True

def main():
    server_brick_address = 'ash-ev3-07'
    # client_mailbox_name = 'client0'
    client_mailbox_name = 'client1'
    GRID_SIZE = 5


    print("starting bluetooth client...")
    client = connect_to_bluetooth_server(server_brick_address)

    print("Receiving Bluetooth handshake...")
    client_mailbox = create_mailbox(client_mailbox_name, client)
    print("Connected")
 

    farm_space = initialize_client_world(grid_size=GRID_SIZE)
    print_world(farm_space)

    # initial_position = (0, 0, 0)
    initial_position = (4, 0, 0)

    print("Sending initial position to server...")
    send_initial_client_position(client_mailbox, initial_position)
    print("Position sent.")

    print("Waiting for task from server...")
    fruit_location = decode_message(client_mailbox.read())
    print("Received task:", fruit_location)

    if fruit_location:
        # Execute path planning and fruit collection logic
        print("Executing task...")
        # task_success = pickup_fruit(initial_position, fruit_location, farm_space)
        task_success = pickup_fruit_and_return(initial_position, fruit_location, initial_position, farm_space)

        # Update the server with the task status
        if task_success:
            status = 'free'
            task_state = 'completed'
            print("Task completed.")
        else:
            status = 'free'
            task_state = 'failed'
            print("Task failed.")

    print("Client script ending.")

if __name__ == "__main__":
    main()
    # open_gripper()
    # close_gripper()