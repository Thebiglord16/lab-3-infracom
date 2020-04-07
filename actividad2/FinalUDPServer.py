from socket import *
import socket
import hashlib
import logging
import logging.handlers
import time
import os

LOG_FILENAME = 'UDPserverLog.log'
logger = logging.getLogger('UDPserverLogger')
logger.setLevel(logging.INFO)
handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, mode='w', backupCount=50)
logging_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setLevel(logging.INFO)
handler.setFormatter(logging_format)
logger.addHandler(handler)
logging.handlers.RotatingFileHandler.doRollover(handler)


# Se seclaran el host el puerto de TCP y la cantidad de clientes esperados
route = "./media/bigFile.mp4"
host = input("enter the host address the server will be running on")
print("we will be using the port 65432,and the ports from 20001 to 2000XX where XX is equal to 1+the number of request")
quantity = int(input("enter the amount of request the server will be waiting for"))
portTCP = 65432
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
logger.info("Starting the process of sending a file to the connected clients")
logger.info("Sending file: " + route + " with size: " + str(os.path.getsize("multimedia2.mp4")) + " bytes")
for puerto in portsUDP:

    time.sleep(2)
    portU = puerto.split(":")[1]
    portU = portU.replace("'", "")
    numero = puerto.split(":")[0]
    numero = numero.replace("'", "")
    logger.info("sending file to client: " + numero)
    bufferSize = 1024
    with socket.socket(AF_INET, SOCK_DGRAM) as n:

        addr = (host, int(portU))
        file_name = "multimedia" + str(numero) + ".mp4"
        enviableBytes = str.encode(file_name)
        n.sendto(enviableBytes, addr)

        f = open("multimedia2.mp4", "rb")
        data = f.read(bufferSize)
        start = time.time()
        while data:
            if n.sendto(data, addr):
                print("Enviando ...")
                data = f.read(bufferSize)
        end = time.time()
        n.close()
        f.close()
    logger.info("sent file to client " + str(numero) + " in " + str(round(end - start, 4)))

