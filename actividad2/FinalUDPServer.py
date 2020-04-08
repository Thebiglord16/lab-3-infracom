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
route = ""
archivo = input("write 1 to select the little file or 2 to select the big file")
bufferUDP = 1024
if archivo == "1":
    route = "./archivos/archivo.w3speech"
    bufferUDP = 40960
    nombre = "archivo"
    ext = ".w3speech"
else:
    route = "./archivos/multimedia.mp4"
    bufferUDP = 10240
    nombre = "multimedia"
    ext = ".mp4"
tamanio = int(os.path.getsize(route))
cantidadEnviables= int(tamanio/bufferUDP)+1

print(route)

host = input("enter the host address the server will be running on")
print("we will be using the port 65432,and the ports from 20001 to 200XX where XX is equal to 1+the number of request")
quantity = int(input("enter the amount of request the server will be waiting for"))
portTCP = 65432
portsUDP = []

hasher = hashlib.md5()
with open(route, 'rb') as afile:
    buf = afile.read(1024)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(1024)
hashEsperado = hasher.hexdigest()

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
        conn.send(bytes(str(hashEsperado+":::"+str(tamanio)), encoding='utf8'))

    s.close()
# Se selecciona cada puerto individual y se comienza la transmision de datos
logger.info("Starting the process of sending a file to the connected clients")
logger.info("Sending file: " + route + " with size: " + str(os.path.getsize(route)) + " bytes")
logger.info("We will send "+ str(cantidadEnviables)+" packages of " + str(bufferUDP)+" bytes")
for puerto in portsUDP:

    time.sleep(2)
    portU = puerto.split(":")[1]
    portU = portU.replace("'", "")
    numero = puerto.split(":")[0]
    numero = numero.replace("'", "")
    numero = numero.replace("b", "")
    logger.info("sending file to client: " + numero)

    with socket.socket(AF_INET, SOCK_DGRAM) as n:

        addr = (host, int(portU))
        file_name = nombre + str(numero) + ext
        enviableBytes = str.encode(file_name)
        n.sendto(enviableBytes, addr)
        f = open(route, "rb")
        data = f.read(bufferUDP)
        start = time.time()
        while data:
            if n.sendto(data, addr):
                print("Enviando ...")
                data = f.read(bufferUDP)
        end = time.time()
        resp = n.recvfrom(1024)[0]
        resp = str(resp).replace("'", "")
        resp = resp.replace("b", "")
        logger.info("Was the Hash test successful: " + resp)
        n.close()
        f.close()
    logger.info("sent file to client " + str(numero) + " in " + str(round(end - start, 4)))
