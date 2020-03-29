import os
import socket
import hashlib

route = "./media/nvm.mp4"
host = input("enter the host address the server will be running on")
port = int(input("enter the port where the server will be listening for requests"))
quantity = int(input("enter the amount of request the server will be waiting for"))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()
    connected_clients = []
    readSize = 1024000
    fileHash = hashlib.md5()
    with open(route, 'rb') as file:
        fb = file.read(readSize)
        while len(fb) > 0:
            fileHash.update(fb)
            fb = file.read(readSize)
    bytesHash = fileHash.digest()
    while True:
        conn, addr = s.accept()
        connected_clients.append(conn)
        print("Connected by ", addr)
        data = conn.recv(1024)
        print("El cliente dijo: ", repr(data))
        message = "Waiting for other clients " + str(len(connected_clients)) + " of " + str(quantity)
        conn.send(bytes(message, encoding='utf8'))
        if len(connected_clients) == quantity:
            for client in connected_clients:
                size = os.path.getsize(route)
                client.send(int.to_bytes(size, 64, byteorder='big'))
                client.send(bytesHash)
                f = open(route, 'rb')
                package = f.read(1024000)
                while package:
                    client.send(package)
                    package = f.read(1024000)
                f.close()
                print("Fisnished sending the file")
                final_confirmation = client.recv(1024)
                print("The client finished writing the file with", repr(final_confirmation))
                client.close()


def write_in_log(message):
    return
