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
    image1 = cv2.imread("/root/images/20.jpeg")
    #crop possibile
    faces1, confidences1 = cv.detect_face(image1)
    counter=len(confidences1)
    # loop through detected faces
    for face,conf in zip(faces1,confidences1):

        (startX,startY) = face[0],face[1]
        (endX,endY) = face[2],face[3]
        #print(startX)
        #print(endX)
        print(endX-startX)
        #print(startY)
        #print(endY)
        print(endY-startY)
        print((endX-startX)*(endY-startY))
        #print("   ###################           ")
        #if endX-startX<
        #draw rectangle over face
        #controllo su y
        if (endX-startX)*(endY-startY)>20000:
           cv2.rectangle(image1, (startX,startY), (endX,endY), (0,255,0), 2)
        else:
            counter-=1

    # save output

    cv2.imwrite("/root/images/20new.jpeg", image1)
    if counter>1:
        counter=1
    return counter

if __name__ == '__main__':

                detected_people=PeopleDetection()

                print(detected_people)
                