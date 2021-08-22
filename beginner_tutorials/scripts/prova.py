#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import subprocess
from sensor_msgs.msg import Image
import random
import socket, select
from time import gmtime, strftime
from random import randint
from cv_bridge import CvBridge
import cv2   
   
def Socket():

       #exec the server
      
       #subprocess.call("/root/images/Server.py", shell=True)
       #rospy.sleep(10)
       #read and convert image
       bridge = CvBridge()
       msg = rospy.wait_for_message('/xtion/rgb/image_raw', Image)
       image = bridge.imgmsg_to_cv2(msg, desired_encoding= "bgr8")
       cv2.imwrite("/root/images/provaimm.jpg", image)
       
       #socket
       HOST = '127.0.0.1'  # The server's hostname or IP address
       PORT = 65432        # The port used by the server

       s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       s.connect((HOST, PORT))
       s.sendall("new_image")
       data = s.recv(4096)
       detected_people=data
       print(detected_people)



if __name__ == '__main__':
       rospy.init_node('talker', anonymous=True)
       print("node")
       Socket()
       

       


