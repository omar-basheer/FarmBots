#!/usr/bin/env pybricks-micropython
from comms import close_bluetooth_connection, create_mailbox, send_server_update_message, start_bluetooth_server, test_handshake, connect_to_bluetooth_server
from farm_helpers import initialize_client_world
from localization import get_current_position

def main():
    server_brick_address = 'ash-ev3-07'
    client_mailbox_name = 'client0'
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

    # step 3: set iniital client state:
    client_status = 'free'
    task_state = 'None'
    position = get_current_position()
    fruit_location = 'None'

    # step3.1: while connection to server is open
    while client:
        # step 3.1.1: send update message to server
        send_server_update_message(client_mailbox, client_mailbox_name, client_status, task_state, position, fruit_location)

        # step 3.1.2: wait for response to message from server
        task_message = client_mailbox.read()
        if task_message:
             # step 3.1.3: update client state:
            client_status = 'busy'
            task_state = 'in progress'
            position = position
            fruit_location = task_message




        # step 3.1.3: execute path planning and fruit collecting
        collect_fruit()






