import socket
import os
import hashlib

idnum = input("input your id number")
host = input("input host please")
port = int(input("input port please"))
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    s.send(b"Ready to receive data")
    data = s.recv(1024)
    print("Received by the client with id " + idnum, repr(data))
    s.send(b"receiving data")
    size = s.recv(1024)
    acSize = int.from_bytes(size, byteorder='big')
    print("preparing to receive a file of size ", acSize)
    acSize = int.from_bytes(size, byteorder='big')
    dataHash = s.recv(1024)

    print("received hash: ", repr(dataHash))
    data = s.recv(1024000)
    route = './media/receivedFlie' + idnum + '.mp4'
    f = open(route, 'wb')
    pCount = 2
    while True:
        f.write(data)
        downloadedSize = os.path.getsize(route)
        print("receiving package, progress " + str((downloadedSize / acSize) * 100) + "%")
        if downloadedSize / acSize == 1.0:
            break
        try:
            data = s.recv(1024000)
            print("packages received: ", pCount)
            pCount += 1
        except Exception as e:
            print(str(e))
            break
    print(os.path.getsize(route) == acSize)
    f.close()
    print("Done receiving data")
