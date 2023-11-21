#!/usr/bin/env pybricks-micropython
# from communications import handshake, start_bluetooth_server, create_mailbox, close_bluetooth_connection, test_handshake
from communications import close_bluetooth_connection, create_mailbox, start_bluetooth_server, handshake, test_handshake
from localization import get_current_position

  
def main():
    # start bluetooth server on Server ev3
    print("starting bluetooth server...")
    server = start_bluetooth_server(client_number=1)

    # Test handshake
    print("initializing bluetooth handshake...")
    # test_handshake(server, None, server_mailbox_name='client', client_mailbox_name='client', client_num=1)
    handshake(server, None, server_mailbox_name='client', client_mailbox_name='client', client_num=1)

if __name__ == "__main__":
   main()
