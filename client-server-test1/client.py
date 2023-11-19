#!/usr/bin/env python3
import bluetooth

def main():
    # Define the MAC address of the server (central controller)
    server_mac = "00:16:53:3F:15:D7"  # Replace with the server's Bluetooth MAC address
    port = 1  # RFCOMM port

    # Set up the Bluetooth client socket
    client_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    client_socket.connect((server_mac, port))

    # For testing purposes, receive a simple message from the server
    message = client_socket.recv(1024)
    print("Client: Received message from server: {}".format(message.decode()))

    # Close the connection
    client_socket.close()

if __name__ == "__main__":
    main()

