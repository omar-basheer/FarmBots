#!/usr/bin/env pybricks-micropython
import math
import time
from communication import create_mailbox, decode_message, send_client_task_message, start_bluetooth_server
from farm import initialize__server_world
from collections import deque
# from pybricks import ev3brick as brick

# queue to track incoming client messages
client_updates_queue = deque()
# dictionary to track the state of each fruit
fruit_state = {}
# set to track assigned fruits
assigned_fruits = set()

def initialize_fruit_state(farm_space):
    """
    Initializes the state of fruits in the farm space.

    Parameters:
    - farm_space (list): 2D list representing the farm space with cell contents.

    Returns:
    int: The count of initialized fruits.
    """
    fruit_count = 0 

    for row in range(len(farm_space)):
        for col in range(len(farm_space[row])):
            cell_content = farm_space[row][col]
            if 'f' in cell_content:
                fruit_state[(row, col)] = {'color': cell_content.split('_')[1], 'picked': False, 'assigned_agent': None}
                fruit_count += 1  

    return fruit_count


def print_world(farm_space):
    for row in farm_space:
        print(" ".join(map(str, row)))


def print_fruit_state():
    """
    Prints the fruit state in key-value pairs line by line.
    """
    print("Fruit State:")
    for location, state in fruit_state.items():
        print("Location: {}, Color: {}, Picked: {}, Assigned Agent: {}".format(
            location, state['color'], state['picked'], state['assigned_agent']
        ))

def assign_task(client_name, client_position):
    """
    Assigns a task to a client based on the current fruit state and the client's position.

    Parameters:
    - client_name (str): The name of the client to assign the task.
    - client_position (tuple): The (x, y) position of the client.

    Returns:
    tuple or None: The location of the assigned fruit or None if no task is available.
    """
    optimal_task = None
    shortest_distance = float('inf')

    for fruit_location, state in fruit_state.items():
        if not state['picked'] and fruit_location not in assigned_fruits:
            # Calculate Euclidean distance between client and fruit
            distance = math.sqrt((client_position[0] - fruit_location[0]) ** 2 +
                                 (client_position[1] - fruit_location[1]) ** 2)

            # Update optimal_task if the distance is shorter
            if distance < shortest_distance:
                shortest_distance = distance
                optimal_task = fruit_location

    if optimal_task:
        fruit_state[optimal_task]['assigned_agent'] = client_name
        assigned_fruits.add(optimal_task)

    return optimal_task

def process_client_positions(client_positions):
    """
    Processes client positions and assigns optimal tasks.

    Parameters:
    - client_positions (dict): Dictionary mapping client names to their positions.

    Returns:
    dict: Dictionary mapping client names to their assigned tasks.
    """
    assigned_tasks = {}

    for client_name, position in client_positions.items():
        assigned_task = assign_task(client_name, position)
        assigned_tasks[client_name] = assigned_task

    return assigned_tasks


def main():
    server_mailbox_name = client_mailbox_name = 'client'
    client_num = 2
    GRID_SIZE = 5
    fruit_map = {
        (2, 3): 'red', 
        (1, 2): 'green', 
        # (4, 2): 'yellow'
        }
    
    print("starting bluetooth server...")
    server = start_bluetooth_server(client_number=client_num)

    print("initializing bluetooth handshake...")
    server_mailboxes = {client_mailbox_name + str(i): create_mailbox(server_mailbox_name + str(i), server) for i in range(client_num)}
    print("connected")

    farm_space = initialize__server_world(fruit_map, grid_size=GRID_SIZE)
    print_world(farm_space)
    fruit_number = initialize_fruit_state(farm_space=farm_space)
    print_fruit_state()
    print("number of fruits: " + str(fruit_number))

    # Introduce a delay for clients to send initial messages
    time.sleep(5)
    # Step 1: Clients send their positions to the server

    client_positions = {}
    for client_mailbox_name, server_mailbox in server_mailboxes.items():
        received_message = server_mailbox.read()
        if received_message:
            client_positions[client_mailbox_name] = decode_message(received_message)
    print(client_positions)

    # Step 2: Server processes client positions and assigns optimal tasks
    assigned_tasks = process_client_positions(client_positions)
    print(assigned_tasks)

    # Step 3: Server sends tasks to clients
    for client_mailbox_name, task_location in assigned_tasks.items():
        send_client_task_message(server_mailboxes[client_mailbox_name], task_location)
        print("Assigned task to " + client_mailbox_name +": " + "Go to fruit at " + str(task_location))

    print("end server script")


if __name__ == "__main__":
   main()