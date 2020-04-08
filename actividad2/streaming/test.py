import threading
import numpy as np
import cv2
import easygui
import shutil
import os
import os.path as ph


def image():
    img = cv2.imread('fondo.jpg', cv2.IMREAD_COLOR)
    cv2.imshow('image', img)
    k = cv2.waitKey(0)
    cv2.destroyWindow('image')


def stream():
    cap = cv2.VideoCapture('1.mp4')
    playing = True
    while (cap.isOpened() & playing):
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        k = cv2.waitKey(50)
        if k == ord('q'):
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
                    break
    cap.release()
    cv2.destroyWindow('frame')


r=easygui.fileopenbox('escoje','file','*',None,False)
d = os.getcwd()+'\\'+ph.basename(r)
print(d)
shutil.copyfile(r,d)
