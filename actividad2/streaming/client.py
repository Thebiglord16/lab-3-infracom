import threading
import csv
import numpy as np
import cv2
import socket
import easygui

canales={}

with open('canales.txt') as f:
    r=csv.reader(f,delimiter=',')
    l=0
    for row in r:
        canales[row[1]] = int(row[0])
    print(canales)



def image(img,count):
    cv2.imshow(str(count),img)
    k=cv2.waitKey(0)
    cv2.destroyWindow('image')


def stream(lista,con):
    playing = True
    f=0
    while (playing):
        if(len(lista)>f):
            frame=lista[f]
            f+=1
            cv2.imshow('frame', frame)
            k = cv2.waitKey(50)
            if k == ord('q'):
                con[0]=False
                break
            elif k == ord('p'):
                print('wait')
                pause = True
                while(pause):
                    p = cv2.waitKey(0)
                    if p == ord('p'):
                        print('ready')
                        pause = False
                    elif p == ord('q'):
                        playing = False
                        con[0]=False
                        break
    cv2.destroyWindow('frame')

udpCS= socket.socket(family=socket.AF_INET,type=socket.SOCK_DGRAM)
udpCS.bind(('127.0.0.1', 60380))
bufferSize=310000
host = '127.0.0.1'
while True:
    msg="Escoja que desea ver"
    title="Seleccion Canal"
    choices=canales.keys()
    choice = easygui.choicebox(msg, title, choices)
    port = int(canales[choice])
    adt='uint8'
    ash=(240, 426, 3)
    r=0
    v=b''
    l=[]
    conn =[True]
    threading.Thread(target=stream,args=(l,conn)).start()
    udpCS.sendto(b'i',(host,port))
    while conn[0]:
        msg=udpCS.recvfrom(bufferSize)
        r+=1
        v+=msg[0]
        print(r)
        if(r==5):
            print('entro')
            m=np.frombuffer(v,dtype=adt).reshape(ash)
            l.append(m)
            r=0
            v=b''
    udpCS.sendto(b's', (host, port))
