#!/usr/bin/env python3

import random
import socket, select
from time import gmtime, strftime
from random import randint
import cv2
import subprocess
import cvlib as cv
import os

            
def PeopleDetection():
    image = cv2.imread("/root/images/provaimm.jpg")

    # apply face detection
    faces, confidences = cv.detect_face(image)

    print(faces)
    print(confidences)

    # loop through detected faces
    for face,conf in zip(faces,confidences):

        (startX,startY) = face[0],face[1]
        (endX,endY) = face[2],face[3]

        # draw rectangle over face
        cv2.rectangle(image, (startX,startY), (endX,endY), (0,255,0), 2)

    # save output
    cv2.imwrite("/root/images/P10.jpg", image)
    if len(confidences)==0:
        return 0
    else:
        return len(confidences)

if __name__ == '__main__':

    HOST = '127.0.0.1'  
    PORT = 65432        
    print("1")
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("2")
    s.bind((HOST, PORT))
    print("3")
    s.listen()
    print("4")
    conn, addr = s.accept()
    print("5")
    with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(4096)
                print(data.decode())
                if not data:
                    break
                
                detected_people=PeopleDetection()
                detected_people=str(detected_people)
                conn.sendall(detected_people.encode())