import pickle
from localization import get_current_position
from pybricks.messaging import BluetoothMailboxServer, BluetoothMailboxClient, Mailbox
from pybricks import ev3brick as brick
import time
from collections import deque

def start_bluetooth_server(client_number):
    """
    Starts a Bluetooth mailbox server and waits for the specified number of clients to connect.

    Parameters:
    - client_number (int): The number of clients to wait for.

    Returns:
    BluetoothMailboxServer: The initialized Bluetooth mailbox server.
    """
    server = BluetoothMailboxServer()
    print("waiting for client(s) to connect...")
    server.wait_for_connection(client_number)
    print('connected!')
    return server

def connect_to_bluetooth_server(server_brick_address):
    """
    Connects to a Bluetooth mailbox server with the given brick address.

    Parameters:
    - server_brick_address (str): The brick address of the server.

    Returns:
    BluetoothMailboxClient: The initialized Bluetooth mailbox client.
    """
    client = BluetoothMailboxClient()
    print("establishing connection with server...")
    client.connect(server_brick_address)
    print('connected!')
    return client

def close_bluetooth_connection(connection):
    connection.close()

def create_mailbox(name, connection):
    """
    Creates and returns a TextMailbox associated with the given name and connection.

    Parameters:
    - name (str): The name of the mailbox.
    - connection: The Bluetooth connection to associate with the mailbox.

    Returns:
    Mailbox: The initialized Mailbox.
    """
    mailbox = Mailbox(name, connection)
    return mailbox

def encode_message(message):
    """
    Encode a Python message into bytes using pickle.

    Parameters:
    - message (any): The Python object to be encoded.

    Returns:
    bytes: The encoded bytes.
    """
    return pickle.dumps(message)

def decode_message(encoded_message):
    """
    Decode bytes into a Python object using pickle.

    Parameters:
    - encoded_message (bytes): The encoded bytes.

    Returns:
    any: The decoded Python object.
    """
    return pickle.loads(encoded_message)

def send_server_update_message(client_mailbox, client_mailbox_name, status, task_state, position, fruit_location):
    """
    Sends an update message to the client mailbox on the server.

    Parameters:
    - client_mailbox: The client's TextMailbox on the server.
    - client_mailbox_name (str): The name of the client mailbox.
    - status (str): The status update of the client (free, busy).
    - task_state (str): The task state update (completed, in progress).
    - position (str): The position update of the client (x, y, theta).
    - fruit_location (str): The assigned fruit location update (x, y).
    """
    # update_message = "Update: Status=" + status + ",Task State=" +task_state+ ",Position=" + position + ",Assigned Fruit Location=" + fruit_location
    message_data = [status, task_state, position, fruit_location]
    encoded_message = encode_message(message_data)
    client_mailbox.send(encoded_message)
    client_mailbox.wait()

def send_client_task_message(client_mailbox, client_mailbox_name, task_message):
    """
    Sends a task message from the server to the client mailbox.

    Parameters:
    - client_mailbox: The client's TextMailbox.
    - client_mailbox_name (str): The name of the client mailbox.
    - task_message (str): The task message to send (x,y).
    """
    message_data = task_message
    encoded_message = encode_message(message_data)
    client_mailbox.send(encoded_message)
    client_mailbox.wait()

def send_position_updates(client_mailbox, client_id):
    x, y, theta = get_current_position()
    message_to_send = "Current Position: "+ client_id + ", X=" + str(x) + ", Y= " + str(y) + ", Theta= " + str(theta) 
    client_mailbox.send(message_to_send)


def test_handshake(server, client, server_mailbox_name, client_mailbox_name, client_num):
    """
    Performs a handshake test between a server and one or more clients.

    Parameters:
    - server: The Bluetooth mailbox server.
    - client: The Bluetooth mailbox client.
    - server_mailbox_name (str): The base name for server mailboxes.
    - client_mailbox_name (str): The name of the client mailbox.
    - client_num (int): The number of client mailboxes to create.
    """
    if server:
        for i in range(client_num):
            #create dedicated mailbox on server
            server_mailbox = create_mailbox(server_mailbox_name + str(i), server)
            print("created mailbox:" + server_mailbox_name + str(i))
        time.sleep(5)

    if client:
        #create a dedicated mailbox on the client
        client_mailbox = create_mailbox(client_mailbox_name, client)
        print(client_mailbox)

        #send a message to server
        # client_id = brick.bluetooth.name
        message_to_send = "hello, server! This is " + client_mailbox_name
        client_mailbox.send(message_to_send)

    if server:
        #receive message from client
        received_message = server_mailbox.read()
        print("Received message from client: "+ received_message)
        brick.display.text(received_message)

    # close_bluetooth_connection(server)
    # close_bluetooth_connection(client)











