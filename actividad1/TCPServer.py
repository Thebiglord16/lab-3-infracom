import os
import socket
import hashlib
import logging
import logging.handlers
import time

LOG_FILENAME = 'tcpserverLog.log'
logger = logging.getLogger('tcpserverLogger')
logger.setLevel(logging.INFO)
handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, mode='w', backupCount=50)
logging_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setLevel(logging.INFO)
handler.setFormatter(logging_format)
logger.addHandler(handler)
logging.handlers.RotatingFileHandler.doRollover(handler)

route = "./media/bigFile.mp4"
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
        logger.info("A client connected, waiting for missing clients " + str(len(connected_clients)) + " of "
                    + str(quantity))
        message = "Waiting for other clients " + str(len(connected_clients)) + " of " + str(quantity)
        conn.send(bytes(message, encoding='utf8'))
        sent = 0
        if len(connected_clients) == quantity:
            logger.info("Starting the process of sending a file to the connected clients")
            logger.info("Sending file: " + route + " with size: " + str(os.path.getsize(route)) + " bytes")
            start_transmission = time.time()
            for client in connected_clients:
                logger.info("sending file to client: " + str(sent))
                start = time.time()
                size = os.path.getsize(route)
                client.send(int.to_bytes(size, 64, byteorder='big'))
                client.send(bytesHash)
                f = open(route, 'rb')
                package = f.read(1024000)
                p_count = 1
                while package:
                    client.send(package)
                    p_count += 1
                    package = f.read(1024000)
                f.close()
                print("Fisnished sending the file")
                final_confirmation = client.recv(1024)
                end = time.time()
                print("The client: " + str(sent) + " finished writing the file in " + str(round(end - start, 4)) +
                      "s with", repr(final_confirmation))
                logger.info("sent file to client " + str(sent) + " in " + str(round(end - start, 4)) + "s with " +
                            repr(final_confirmation) + "s, packages sent: " + str(p_count))

                sent += 1
        if sent == quantity:
            end_transmission = time.time()
            print("Server finished all tasks in " + str(round(end_transmission - start_transmission, 4)) + "s")
            print("Shutting down...")
            logger.info("Finished delivery to " + str(quantity) + " clients within " +
                        str(round(end_transmission - start_transmission, 4)) + "s")
            break
