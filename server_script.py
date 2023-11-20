from WirelessComm.communications import start_bluetooth_server, create_mailbox, close_bluetooth_connection, test_handshake

def main():
    # start bluetooth server on Server ev3
    server = start_bluetooth_server(client_number=1)

    # Test handshake
    test_handshake(server, None, server_mailbox_name='handshake', client_mailbox_name='handshake')

    # # start bluetooth server on Server ev3
    # server = start_bluetooth_server(client_number=1)

    # #create a dedicated mailbox on the server
    # server_mailbox_name = 'handshake'
    # server_mailbox = create_mailbox(server_mailbox_name, server)

    # #wait for client(s) to connect
    # print("waiting for client(s) to connect...")
    # server.wait_for_connection()

    # #receive message from client
    # received_message = server_mailbox.read()
    # print(f"Received message from client: {received_message}")

    # #close bluetooth connection
    # close_bluetooth_connection(server)



if __name__ == "__main__":
    main()
