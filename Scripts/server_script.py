from WirelessComm.communications import handshake, start_bluetooth_server, create_mailbox, close_bluetooth_connection, test_handshake

def main():
    # start bluetooth server on Server ev3
    server = start_bluetooth_server(client_number=1)

    # Test handshake
    test_handshake(server, None, server_mailbox_name='client', client_mailbox_name='client', client_num=1)
    handshake(server, None, server_mailbox_name='client', client_mailbox_name='client', client_num=1)

if __name__ == "__main__":
    main()
