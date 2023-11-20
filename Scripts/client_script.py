from WirelessComm.communications import connect_to_bluetooth_server, create_mailbox, close_bluetooth_connection, handshake, test_handshake

def main():
    server_brick_address = 'ash-ev3-07'

    # Connect to Bluetooth server on Server EV3
    client = connect_to_bluetooth_server(server_brick_address)

    # Test handshake
    test_handshake(None, client, server_mailbox_name='client1', client_mailbox_name='client1', client_num=0)
    handshake(None, client, server_mailbox_name='client1', client_mailbox_name='client1', client_num=0)


if __name__ == "__main__":
    main()