from WirelessComm.communications import connect_to_bluetooth_server, create_mailbox, close_bluetooth_connection, test_handshake

def main():
    server_brick_address = 'ash-ev3-07'

    # Connect to Bluetooth server on Server EV3
    client = connect_to_bluetooth_server(server_brick_address)

    # Test handshake
    test_handshake(None, client, server_mailbox_name='handshake', client_mailbox_name='handshake')

    
    # server_brick_address = 'ash-ev3-07'

    # #connect to bluetooth server on Server ev3
    # client = connect_to_bluetooth_server(server_brick_address)

    # #create a dedicated mailbox on the client
    # client_mailbox_name = 'handshake'
    # client_mailbox = create_mailbox(client_mailbox_name, client)

    # #send message to server
    # message_to_send = "hello, server!"
    # client_mailbox.send(message_to_send)

    # #close the connection
    # close_bluetooth_connection(client)

if __name__ == "__main__":
    main()