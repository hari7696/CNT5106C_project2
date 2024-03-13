import socket
import time
import sys


def main(port):

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostbyname(socket.gethostname())
    print("CONNECTION ESTABLISHED WITH SERVER {} ON PORT {}".format(host, port))
    client.connect((host, port))

    while True:

        command = input("Enter command: ")

        if command.startswith("exit"):
            client.send("exit".encode("utf-8"))
            client.shutdown(2)
            client.close()
            break

        if command.startswith("quit"):
            client.send("quit".encode("utf-8"))
            client.shutdown(2)
            client.close()
            break


        elif command.startswith("upload"):
            file_name = command.split(" ")[1]

            # upload file to server
            client.send(f"server_recieve {file_name}".encode("utf-8"))

            filetoupload = open(file_name, "rb")
            data = filetoupload.read(1024)
            while data:

                client.send(data)
                data = filetoupload.read(1024)

            client.send(b"EOF")
            filetoupload.close()
            print("Done Sending.")
            print("STATUS: File Uploaded.")

        elif command.startswith("get"):
            file_name = command.split(" ")[1]
            # download filename.txt
            client.send(f"server_send {file_name}".encode("utf-8"))
            filetodown = open("new" + file_name, "wb")
            while True:
                data = client.recv(1024)
                # checking for end of file
                if data[-3:] == b"EOF":

                    data = data[:-3]
                    filetodown.write(data)
                    filetodown.close()
                    print("Done Receiving.")
                    break
                filetodown.write(data)

            print("STATUS: File Downloaded.")

        else:
            print(
                "Invalid command entered, please choose from following [upload filename, get filename, exit]"
            )


if __name__ == "__main__":

    if len(sys.argv) > 1:
        arg = sys.argv[1]
        port = int(arg)
    else:
        print("No command line argument provided. choosing default 5106 port")
        port = 5106

    main(port)
