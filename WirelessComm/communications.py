from localization import get_current_position
from pybricks.messaging import BluetoothMailboxServer, BluetoothMailboxClient, TextMailbox, Mailbox
from pybricks import ev3brick as brick
import time

def start_bluetooth_server(client_number):
    server = BluetoothMailboxServer()
    print("waiting for client(s) to connect...")
    server.wait_for_connection(client_number)
    print('connected!')
    return server

def connect_to_bluetooth_server(server_brick_address):
    client = BluetoothMailboxClient()
    print("establishing connection with server...")
    client.connect(server_brick_address)
    print('connected!')
    return client

def close_bluetooth_connection(connection):
    connection.close()

def create_mailbox(name, connection):
    # mailbox = Mailbox(name, connection)
    mailbox = TextMailbox(name, connection)
    return mailbox

def  send_message_to_client(mailbox, message, client_address):
    mailbox.send(message, brick=client_address)

def send_message_to_server(mailbox, message):
    mailbox.send(message)

# def send_position_updates(client_mailbox, client_id):
#     for i in range(10):
#         x, y, theta = get_current_position()

#         # Include client identifier in the position update message
#         message_to_send = "Position Update from "+ client_mailbox_name + ", X=" + str(x) + ", Y= " + str(y) + ", Theta= " + str(theta) 
#         client_mailbox.send(message_to_send)

#         # Wait for a short interval before sending the next update
#         time.sleep(1)

def test_handshake(server, client, server_mailbox_name, client_mailbox_name, client_num):
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

def handshake(server, client, server_mailbox_name, client_mailbox_name, client_num):
    if server: 
        #create dedicated mailbox on server
        server_mailboxes = [create_mailbox(server_mailbox_name + str(i), server) for i in range(client_num)]
        time.sleep(5)

    if client:
        #create a dedicated mailbox on the client
        client_mailbox = create_mailbox(client_mailbox_name, client)
        print(client_mailbox)

        # Send position updates from the client to the server
        for i in range(5):
            x, y, theta = get_current_position()
            # Include client identifier in the position update message
            message_to_send = "Position Update from "+ client_mailbox_name + ", X=" + str(x) + ", Y= " + str(y) + ", Theta= " + str(theta) 
            client_mailbox.send(message_to_send)
            time.sleep(2)

    if server:
        # Iterate over each server mailbox and read messages
        for i, server_mailbox in enumerate(server_mailboxes):
            print()
            for j in range(5):
                #receive message from client
                received_message = server_mailbox.read()
                if received_message:
                    print("Received message from client: "+ received_message)
                    brick.display.text(received_message)
                else:
                    print("no update")
                    brick.display.text("no update")

                # Wait for a short interval before sending the next update
                time.sleep(1)






