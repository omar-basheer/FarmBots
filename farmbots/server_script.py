#!/usr/bin/env pybricks-micropython
from comms import close_bluetooth_connection, create_mailbox, decode_message, send_client_task_message, start_bluetooth_server, test_handshake
from farm_helpers import initialize__server_world
from localization import get_current_position
import queue
from collections import deque
import time

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

def assign_task(client_name):
    """
    Assigns a task to a client based on the current fruit state.

    Parameters:
    - client_name (str): The name of the client to assign the task.

    Returns:
    tuple or None: The location of the assigned fruit or None if no task is available.
    """
    for fruit_location, state in fruit_state.items():
        if not state['picked'] and fruit_location not in assigned_fruits:
            state['assigned_agent'] = client_name
            assigned_fruits.add(fruit_location)
            return fruit_location

def reassign_task(client_name, fruit_location):
    return fruit_location

def assign_new_task(client_name):
    pass


def process_message(client_name, message, fruit_number):
    """
    Processes a message from a client, updating the fruit state and assigning tasks accordingly.

    Parameters:
    - client_name (str): The name of the client sending the message.
    - message (str): The message received from the client.

    Returns:
    tuple or None: The location of the assigned task or None.
    """

     # Convert string of list back to list
    print("processing message...")
    message_list = decode_message(message)

    status, task_state, client_position, fruit_location = message_list

    if  fruit_location:
        fruit_state[fruit_location]['picked'] = True if task_state == 'completed' else False
        # fruit_number = fruit_number -1 if task_state == 'completed' else fruit_number
        fruit_state[fruit_location]['assigned_agent'] = client_name 
        if task_state == 'completed' and fruit_state[fruit_location]['picked']:
            # global fruit_number 
            fruit_number -= 1
    print("current fruit states...")
    print_fruit_state()

    if fruit_number == 0:
        return None

    if status == 'free':
        # client is waiting for fresh task to execute
        assigned_task = assign_task(client_name)
        if assigned_task: 
            print("Assigned task to " + client_name +": " + "Go to fruit at " + str(assigned_task))
            return assigned_task
        
    elif status == 'busy' and task_state == 'in progress':
        # client is waiting for redirection
        reassigned_task = reassign_task(client_name, fruit_location)
        if reassigned_task: 
            print("Reassigned task to " + client_name +": " + "Go to fruit at " + str(reassigned_task))
            return reassigned_task
    

 
def main():
    server_mailbox_name = client_mailbox_name = 'client'
    client_num = 2
    GRID_SIZE = 12
    fruit_map = {
        (2, 3): 'red', 
        (5, 8): 'green', 
        (9, 4): 'yellow'
        }

    # step 1: connect to clients
    print("starting bluetooth server...")
    server = start_bluetooth_server(client_number=client_num)

    print("initializing bluetooth handshake...")
    server_mailboxes = {client_mailbox_name + str(i): create_mailbox(server_mailbox_name + str(i), server) for i in range(client_num)}
    print("connected")
    # time.sleep(5)

    # step 2: initialize world for server
    farm_space = initialize__server_world(fruit_map, grid_size=GRID_SIZE)
    print_world(farm_space)
    fruit_number = initialize_fruit_state(farm_space=farm_space)
    
    # step 3: while all fruits are not collected...
    while fruit_number > 0:
    # step 3.1: queue update messages from clients
        for client_mailbox_name, server_mailbox in server_mailboxes.items():
            received_message = server_mailbox.read()
            if received_message:
                client_updates_queue.append((client_mailbox_name, received_message))
                print("new update message from " + client_mailbox_name)
                print(client_updates_queue)
    
        #step 3.2: process messages in queue
        while client_updates_queue:
            # print("reading a message...")
            client_name, message = client_updates_queue.popleft()
            assigned_fruit_location = process_message(client_name, message, fruit_number)
            if assigned_fruit_location:
                task_message = assigned_fruit_location
                send_client_task_message(server_mailboxes[client_name], client_name, task_message)
            else:
                # no more fruits to collect
                print("all fruits collected successfully, program ending...")
                fruit_number = 0
    
        time.sleep(5)
    # close_bluetooth_connection(server)
        


if __name__ == "__main__":
   main()



