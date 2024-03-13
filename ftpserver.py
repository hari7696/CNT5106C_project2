import socket
import threading
import os
import sys
import socket
import threading
import os
import sys


# Global variable to keep track of active connections
active_connections = 0

def handle_client(clientSocket, addr, quit_status,active_connections):

    # clientSocket.send("Thank you for connecting".encode("utf-8"))
    while True:

        data = clientSocket.recv(1024)
        decoded_message = data.decode("utf-8")

        if decoded_message == "quit":
            print(f"Client {addr} disconnected")
            active_connections = active_connections - 1
            #print("number of active connectons", active_connections)
            if active_connections == -1:
                print("No active connections. Server shutting down.")
                quit_status = True
                os._exit(1)
            break

        if decoded_message == "exit":
            active_connections = active_connections - 1
            print(f"Client {addr} disconnected")
            break

        if decoded_message.startswith("server_recieve"):

            # recieves the file from client

            file_name = decoded_message.split(" ")[1]
            filetodown = open("new" + file_name, "wb")
            while True:
                data = clientSocket.recv(1024)
                # checking for end of file
                if data[-3:] == b"EOF":
                    data = data[:-3]
                    filetodown.write(data)
                    filetodown.close()
                    print("Done Receiving.")
                    break
                filetodown.write(data)
            print("STATUS: File Downloaded.")

            # clientSocket.close()

        if decoded_message.startswith("server_send"):
            file_name = decoded_message.split(" ")[1]
            # send the file to client

            filetoupload = open(file_name, "rb")
            data = filetoupload.read(1024)
            while data:

                clientSocket.sendall(data)
                data = filetoupload.read(1024)

            clientSocket.send(b"EOF")
            filetoupload.close()
            print("Done Sending.")
            print("STATUS: File Uploaded.")

    clientSocket.close()


def main(port):
    global active_connections
    global quit_status
    quit_status = False
    active_connections = 0

    # Create a socket object
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = socket.gethostbyname(socket.gethostname())
    serverSocket.bind((host, port))

    # Now wait for client connection.
    serverSocket.listen(5)
    print(f"SERVER STARTED Actively Listening on {host}:{port}")

    while True:
        # Establish connection with client.
        clientSocket, addr = serverSocket.accept()
        #print("Main program", quit_status)
        thread = threading.Thread(target=handle_client, args=(clientSocket, addr, quit_status,active_connections))
        thread.start()
        active_connections = active_connections + 1
        #print(f"active connections {active_connections}")
        print("Got connection from", addr)
        if quit_status:
            break
    serverSocket.close()


if __name__ == "__main__":

    if len(sys.argv) > 1:
        arg = sys.argv[1]
        port = int(arg)
    else:
        print("No command line argument provided. choosing default 5106 port")
        port = 5106

    main(port)
