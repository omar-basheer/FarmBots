import pickle
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

def send_initial_client_position(client_mailbox, initial_position):
    """
    Sends a task message from the server to the client mailbox.

    Parameters:
    - client_mailbox: The client's TextMailbox.
    - client_mailbox_name (str): The name of the client mailbox.
    - task_message (str): The task message to send (x,y).
    """
    message_data = initial_position
    encoded_message = encode_message(message_data)
    client_mailbox.send(encoded_message)
    client_mailbox.wait()

def send_client_task_message(client_mailbox, task_message):
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
    # client_mailbox.wait()