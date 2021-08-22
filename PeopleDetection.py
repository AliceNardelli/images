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
    image = cv2.imread("/root/images/table5.jpg")

    # apply face detection
    faces, confidences = cv.detect_face(image)

    #print(faces)
    #print(confidences)

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

                detected_people=PeopleDetection()

                print(detected_people)
                