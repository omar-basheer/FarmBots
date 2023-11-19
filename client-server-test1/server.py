#!/usr/bin/env python3
import bluetooth
def main():
    # Set up the Bluetooth server socket
    server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    server_socket.bind(("", bluetooth.PORT_ANY))
    server_socket.listen(1)
    port = server_socket.getsockname()[1]

    uuid = "00001101-0000-1000-8000-00805F9B34FB"  # SPP (Serial Port Profile) UUID
    bluetooth.advertise_service(server_socket, "EV3Server", service_id=uuid)

    print("Server: Waiting for a connection...")
    client_socket, client_info = server_socket.accept()
    print("Server: Accepted connection from {}".format(client_info))

    # For testing purposes, send a simple message to the client
    client_socket.send("Connection successful. Ready to test.")

    # Close the connection
    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    main()

