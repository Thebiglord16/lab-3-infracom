from socket import *
import socket
import os
import hashlib
import threading
# Puerto a partir del cual se comienzan las transmisiones UDP
portUDP = 20000


class ClientThread(threading.Thread):
    idnum = "0"
    portUDP = 0

    def run(self):
        host = "127.0.0.1"
        portTCP = 65432
        # Se comienza la transmision TCP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, portTCP))
            s.send(b"Ready to receive data")
            data = s.recv(1024)
            print(data)
            s.send(str.encode(self.idnum+":"+str(self.portUDP)))
        s.close()

        # Se comienza a recibir el archivo por UDP
        with socket.socket(AF_INET, SOCK_DGRAM) as n:
            bufferSize = 1024
            n.bind((host, self.portUDP))
            addr = (host, self.portUDP)
            data, addr = n.recvfrom(bufferSize)
            print("Se recibio el archivo: ", data.strip())
            f = open(data.strip(), 'wb')

            data, addr = n.recvfrom(bufferSize)
            try:
                while data:
                    f.write(data)
                    n.settimeout(2)
                    data, addr = n.recvfrom(bufferSize)
            except timeout:
                f.close()
                n.close()
                print("Se termino de descargar el archivo")



client_num = 25
clients = []

while len(clients) < client_num:
    client = ClientThread()
    client.idnum = str(len(clients))
    portUDP = portUDP + 1
    client.portUDP = portUDP
    clients.append(client)

for client in clients:
    client.start()
