#!/usr/bin/env pybricks-micropython
import random
import time
from comms import close_bluetooth_connection, create_mailbox, decode_message, send_server_update_message, start_bluetooth_server, test_handshake, connect_to_bluetooth_server
from farm_helpers import initialize_client_world
from localization import get_current_position
from pybricks import ev3brick as brick

def print_world(farm_space):
    for row in farm_space:
        print(" ".join(map(str, row)))

def pickup_fruit(current_position, goal_position):
    # Simulate task planning and execution duration
    planning_duration = 3  # in seconds
    execution_duration = 7  # in seconds

    print("Robot is planning a path from {} to {}.".format(current_position, goal_position))
    time.sleep(planning_duration)
    
    # Simulate execution of the planned path
    print("Robot is executing the planned path...")
    time.sleep(execution_duration)

    # Simulate picking up the fruit - random success or failure
    pickup_success = random.choice([True, False])

    if pickup_success:
        print("Pickup successful!")
    else:
        print("Pickup failed. Retrying...")

    return pickup_success


def main():
    server_brick_address = 'ash-ev3-07'
    client_mailbox_name = 'client1'
    GRID_SIZE = 12
    x, y, theta = 0, 0, 0
    
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
    position = get_current_position()
    fruit_location = None

    # step3.1: while connection to server is open
    while client:
        # step 3.1.1: send update message to server
        print("updating server with current status...")
        send_server_update_message(client_mailbox, client_mailbox_name, client_status, task_state, str(position), fruit_location)
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
            brick.display.text(task_message)

            # step 3.1.3.2: execute path planning and fruit collecting
            print("executing task...")
            task_success = pickup_fruit(position, fruit_location)

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



