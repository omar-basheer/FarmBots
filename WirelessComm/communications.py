from Localization.localization import get_current_position
from pybricks.messaging import BluetoothMailboxServer, BluetoothMailboxClient, TextMailbox, Mailbox
from pybricks import ev3brick as brick
import time

def start_bluetooth_server(client_number):
    server = BluetoothMailboxServer()
    server.wait_for_connection(client_number)
    return server

def connect_to_bluetooth_server(server_brick_address):
    client = BluetoothMailboxClient()
    client.connect(server_brick_address)
    return client

def close_bluetooth_connection(connection):
    connection.close()

def create_mailbox(name, connection):
    mailbox = Mailbox(name, connection)
    return mailbox

def  send_message_to_client(mailbox, message, client_address):
    try:
        mailbox.send(message, brick=client_address)
    except OSError as e:
        print(f"Error sending message: {e}")

def send_message_to_server(mailbox, message):
    try:
        mailbox.send(message)
    except OSError as e:
        print(f"Error sending message to server: {e}")

def send_position_updates(client_mailbox, client_id):
    for i in range(10):
        x, y, theta = get_current_position()

        # Include client identifier in the position update message
        message_to_send = f"Position Update from {client_id}: X={x}, Y={y}, Theta={theta}"
        client_mailbox.send(message_to_send)

        # Wait for a short interval before sending the next update
        time.sleep(1)

def test_handshake(server, client, server_mailbox_name, client_mailbox_name, client_num):
    for i in range(client_num):
        #create dedicated mailbox on server
        server_mailbox = create_mailbox(server_mailbox_name + str(i), server)

    #wait for client(s) to connect
    print("waiting for client(s) to connect...")
    server.wait_for_connection()
    print('connected!')

    #create a dedicated mailbox on the client
    client_mailbox = create_mailbox(client_mailbox_name, client)

    #send a message to server
    # client_id = brick.bluetooth.name
    message_to_send = "hello, server! This is " + client_mailbox_name
    client_mailbox.send(message_to_send)

    #receive message from client
    received_message = server_mailbox.read()
    print(f"Received message from client: {received_message}")

    # close connections
    close_bluetooth_connection(server)
    close_bluetooth_connection(client)

def handshake(server, client, server_mailbox_name, client_mailbox_name, client_num):
    for i in range(client_num):
        #create dedicated mailbox on server
        server_mailbox = create_mailbox(server_mailbox_name + str(i), server)

    #wait for client(s) to connect
    print("waiting for client(s) to connect...")
    server.wait_for_connection()
    print('connected!')

    #create a dedicated mailbox on the client
    client_mailbox = create_mailbox(client_mailbox_name, client)

    # Send position updates from the client to the server
    # send_position_updates(client_mailbox, client_id)
    for i in range(10):
        x, y, theta = get_current_position()

        # Include client identifier in the position update message
        message_to_send = f"Position Update from {client_mailbox_name}: X={x}, Y={y}, Theta={theta}"
        client_mailbox.send(message_to_send)

        #receive message from client
        received_message = server_mailbox.read()
        print(f"Received message from client: {received_message}")

        # Wait for a short interval before sending the next update
        time.sleep(1)






