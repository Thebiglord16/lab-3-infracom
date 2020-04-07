from socket import *
import socket
import time

# Se seclaran el host el puerto de TCP y la cantidad de clientes esperados
host = "127.0.0.1"
portTCP = 65432
quantity = 25
portsUDP = []
# Se realiza una conexion TCP para asegurarse que todos los clientes han llegado y estan listos a recibir
# en este mismo proceso se obtienen los puertos por los que los clientes esperaran la conexion UDP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Se enlace el socket con el host y el puerto TCP
    s.bind((host, portTCP))
    s.listen()
    connected_clients = []
    # Se esperan los multiples clientes, se recibe su confirmacion y su puerto UDP
    while len(connected_clients) < quantity:
        conn, addr = s.accept()
        connected_clients.append(conn)
        print("Connected by ", addr)
        message = "Waiting for other clients " + str(len(connected_clients)) + " of " + str(quantity)
        data = conn.recv(1024)
        if data == str.encode("Ready to receive data"):
            conn.send(bytes(message, encoding='utf8'))
        data = conn.recv(1024)
        portsUDP.append(str(data))
    s.close()
# Se selecciona cada puerto individual y se comienza la transmision de datos
for puerto in portsUDP:

    time.sleep(2)
    portU = puerto.split(":")[1]
    portU = portU.replace("'", "")
    numero = puerto.split(":")[0]
    numero = numero.replace("'", "")
    bufferSize = 1024
    with socket.socket(AF_INET, SOCK_DGRAM) as n:

        addr = (host, int(portU))
        file_name = "multimedia" + str(numero) + ".mp4"
        enviableBytes = str.encode(file_name)
        n.sendto(enviableBytes, addr)

        f = open("multimedia2.mp4", "rb")
        data = f.read(bufferSize)
        while data:
            if n.sendto(data, addr):
                print("Enviando ...")
                data = f.read(buf)
        n.close()
        f.close()
