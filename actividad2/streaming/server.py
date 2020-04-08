import numpy as np
import cv2
import threading
import csv
import socket
import time
import easygui
import shutil
import os
import os.path as ph
host = '127.0.0.1'
bufferSize = 310000
canales = {}
keys= []
end=[True]
def loadCanales():
    with open('canales.txt') as f:
        r = csv.reader(f, delimiter=',')
        for row in r:
            print(row)    
            keys.append(row[1])
            canales[row[1]]=int(row[0])
        print(canales)


def stream(file,ips,udpSS):
    while end[0]:
        cap = cv2.VideoCapture(file)
        while (cap.isOpened()) & end[0]:
            ret, frame = cap.read()
            if frame is None:
                break
            try:
                b = frame.tobytes()
            except:
                print(frame)
            for i in range(0, 5):
                sm = b[61344*i:61344*(i+1)]
                for ip in ips:
                    # try:
                    udpSS.sendto(sm, ip)
                    # except:
                    #     print('dissconected')
                    #     ips.remove(ip)
                time.sleep(0.01)
        cap.release()
        print('fin transmision')
    udpSS.close()


def channel(port,file):
    udpSS = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    udpSS.bind((host, port))
    print('initialized stream channel '+str(port))
    ips=[]
    threading.Thread(target=stream, args=(file,ips,udpSS)).start()
    while end[0]:
        try:
            bites = udpSS.recvfrom(bufferSize)
            if bites[0] == b'i':
                ips.append(bites[1])
            elif bites[0] == b's':
                ips.remove(bites[1])
                print('out')
        except:
            print('someone out')
            ips.clear()

def upload():
    p=0
    while True:
        p=easygui.integerbox("En que puerto lo quiere reproducir",'Puerto',65432,None,None)
        find=True
        for key in keys:
            if canales[key]==p:
                find = False
        if find:
            break
        easygui.ccbox('no se puede repetir el puerto, escoja otro', 'error')    
    r=easygui.fileopenbox('escoje','file','*',None,False)
    n = ph.basename(r)
    d = os.getcwd()+'\\'+n
    shutil.copyfile(r,d)
    with open('canales.txt','w',newline='') as f:
        w=csv.writer(f)
        for key in keys:
            w.writerow([canales[key], key])
        w.writerow([p,n])
    loadCanales()
    threading.Thread(target=channel, args=(p, n)).start()

loadCanales()
for key in keys:
    threading.Thread(target=channel, args=(canales[key], key)).start()

while end[0]:
    opt=easygui.buttonbox("Que desea hacer","Streamer",["Añadir canal","Apagar"])
    print(opt)
    if(opt=='Añadir canal'):
        upload()
    elif(opt=='Apagar'):
        end[0]=False

