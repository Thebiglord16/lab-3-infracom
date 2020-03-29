import socket
import os
import hashlib
import threading


class ClientThread(threading.Thread):
    idnum = "0"

    def run(self):
        host = "127.0.0.1"
        port = 65432
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.send(b"Ready to receive data")
            data = s.recv(1024)
            print("Received by the client with id " + self.idnum, repr(data))
            size = s.recv(1024)
            ac_size = int.from_bytes(size, byteorder='big')
            print("preparing to receive a file of size ", ac_size)
            ac_size = int.from_bytes(size, byteorder='big')
            data_hash = s.recv(1024)

            print("received hash: ", repr(data_hash))
            data = s.recv(1024000)
            route = './media/receivedFlie' + self.idnum + '.mp4'
            f = open(route, 'wb')
            p_count = 2
            while True:
                f.write(data)
                downloaded_size = os.path.getsize(route)
                print("receiving package, progress " + str((downloaded_size / ac_size) * 100) + "%")
                if downloaded_size / ac_size == 1.0:
                    break
                try:
                    data = s.recv(1024000)
                    print("packages received: ", p_count)
                    p_count += 1
                except Exception as e:
                    print(str(e))
                    break
            print(os.path.getsize(route) == ac_size)
            f.close()
            file_hash = hashlib.md5()
            with open(route, 'rb') as file:
                fb = file.read(1024000)
                while len(fb) > 0:
                    file_hash.update(fb)
                    fb = file.read(1024000)
            bytes_hash = file_hash.digest()
            if bytes_hash == data_hash:
                s.send(b'succes')
            else:
                s.send(b'error')
            print("Done receiving data")


client_num = 25
clients = []

while len(clients) < client_num:
    client = ClientThread()
    client.idnum = str(len(clients))
    clients.append(client)

for client in clients:
    client.start()
