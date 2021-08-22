#!/usr/bin/env python
import sys
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from beginner_tutorials.srv import People_detection,People_detectionResponse 
import subprocess
import random
import socket, select
from time import gmtime, strftime
from random import randint
from cv_bridge import CvBridge
import cv2 

def srv_clbk(req):
      
       #exec the server
       subprocess.call("/root/images/Server.py", shell=True)
       
       #read and convert image
       bridge = CvBridge()
       msg = rospy.wait_for_message('/xtion/rgb/image_raw', Image)
       image = bridge.imgmsg_to_cv2(msg, desired_encoding= "bgr8")
       cv2.imwrite("/root/images/provaimm.jpg", image)
       
       #socket
       HOST = '127.0.0.1' 
       PORT = 65432        
       print("pr0")
       s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       print("pr1")
       s.connect((HOST, PORT))
       print("pr2")
       s.sendall("new_image")
       print("pr3")
       data = s.recv(4096)
       detected_people=data.decode()
       print(detected_people)
    
       return People_detectionResponse(int(detected_people))
    

if __name__ == '__main__':

       rospy.init_node('talker', anonymous=True)
       srv = rospy.Service('/people_detection', People_detection, srv_clbk)      
       rospy.spin()