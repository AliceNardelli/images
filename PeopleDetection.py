#!/usr/bin/env python3

import random
import socket, select
from time import gmtime, strftime
from random import randint
import cv2
import subprocess
import cvlib as cv
import os
import numpy as np
from matplotlib import pyplot as plt

threshold=0

def equalize_this(image_file, with_plot=False, gray_scale=False):
    image_src = read_this(image_file=image_file, gray_scale=gray_scale)
    if not gray_scale:
        r_image, g_image, b_image = cv2.split(image_src)

        r_image_eq = cv2.equalizeHist(r_image)
        g_image_eq = cv2.equalizeHist(g_image)
        b_image_eq = cv2.equalizeHist(b_image)

        image_eq = cv2.merge((r_image_eq, g_image_eq, b_image_eq))
        cmap_val = None
    else:
        image_eq = cv2.equalizeHist(image_src)
        cmap_val = 'gray'

    if with_plot:
        fig = plt.figure(figsize=(10, 20))

        ax1 = fig.add_subplot(2, 2, 1)
        ax1.axis("off")
        ax1.title.set_text('Original')
        ax2 = fig.add_subplot(2, 2, 2)
        ax2.axis("off")
        ax2.title.set_text("Equalized")

        ax1.imshow(image_src, cmap=cmap_val)
        ax2.imshow(image_eq, cmap=cmap_val)
        return True
    return image_eq 

def PeopleDetection():
    image1 = cv2.imread("/root/images/I.jpg")
    image1=equalize_this(image1,with_plot=True)
    #crop possibile
    faces1, confidences1 = cv.detect_face(image1,0.18,enable_gpu=True)
    counter=len(confidences1)
    # loop through detected faces
    for face,conf in zip(faces1,confidences1):

        (startX,startY) = face[0],face[1]
        (endX,endY) = face[2],face[3]
        #print(endY-startY)
        if (endY-startY)>threshold:
           cv2.rectangle(image1, (startX,startY), (endX,endY), (0,255,0), 2)
        else:
            counter-=1

    # save output

    cv2.imwrite("/root/images/I.jpg", image1)
    if counter>2:
        counter=2
    return counter

if __name__ == '__main__':

                detected_people=PeopleDetection()

                print(detected_people)
                