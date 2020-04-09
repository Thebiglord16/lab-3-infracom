from socket import *
import socket
import os
import hashlib
import threading

# Puerto a partir del cual se comienzan las transmisiones UDP
portUDP = 20000

host = input("enter the host address to make the connection to the server ")


class ClientThread(threading.Thread):
    idnum = "0"
    host = ""
    portUDP = 0
    hashEsperado = ""
    tamanioFile = 0

    def run(self):

        portTCP = 65432
        # Se comienza la transmision TCP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, portTCP))
            s.send(b"Ready to receive data")
            data = s.recv(1024)
            print(data)
            s.send(str.encode(self.idnum + ":" + str(self.portUDP)))
            data = s.recv(1024)
            self.hashEsperado = str(data).split(":::")[0]
            self.tamanioFile = str(data).split(":::")[1]
            self.tamanioFile = self.tamanioFile.replace("'", "")
            self.hashEsperado = self.hashEsperado.replace("'", "")
            self.hashEsperado = self.hashEsperado[1:len(self.hashEsperado)]
        s.close()

        # Se comienza a recibir el archivo por UDP
        with socket.socket(AF_INET, SOCK_DGRAM) as n:
            self.tamanioFile = int(self.tamanioFile)
            if self.tamanioFile < 105000000:
                bufferSize = 40960
            else:
                bufferSize = 10240
            n.bind((host, self.portUDP))
            addr = (host, self.portUDP)
            data, addr = n.recvfrom(bufferSize)
            nombre = data.strip()
            nombre = str(nombre)
            nombre = nombre.replace("b", "")
            nombre = nombre.replace("'", "")
            print("Se recibio el archivo: ", nombre)
            f = open(data.strip(), 'wb')

            data, addr = n.recvfrom(bufferSize)
            try:
                while data:
                    f.write(data)
                    n.settimeout(2)
                    data, addr = n.recvfrom(bufferSize)
            except timeout:
                f.close()
                print("Se termino de descargar el archivo")
            hasher = hashlib.md5()
            with open(nombre, 'rb') as afile:
                buf = afile.read(1024)
                while len(buf) > 0:
                    hasher.update(buf)
                    buf = afile.read(1024)
            hashRecibido = hasher.hexdigest()
            correcto = hashRecibido == self.hashEsperado
            n.sendto(str.encode(str(correcto)), addr)
            n.close()


client_num = 25
clients = []

while len(clients) < client_num:
    client = ClientThread()
    client.host=host
    client.idnum = str(len(clients))
    portUDP = portUDP + 1
    client.portUDP = portUDP
    clients.append(client)

for client in clients:
    client.start()
