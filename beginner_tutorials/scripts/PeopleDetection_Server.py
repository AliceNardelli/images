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
       #read and convert image
       bridge = CvBridge()
       msg = rospy.wait_for_message('/xtion/rgb/image_raw', Image)
       image = bridge.imgmsg_to_cv2(msg, desired_encoding= "bgr8")
       cv2.imwrite("/root/images/provaimm.jpg", image)
       child_program = subprocess.Popen("/root/images/PeopleDetection.py",
                                 shell=True,
                                 stdout=subprocess.PIPE,
                                 )
       
       detected_people = child_program.communicate()
       print(detected_people[0])  
       return People_detectionResponse(int(detected_people[0]))
    

if __name__ == '__main__':

       rospy.init_node('talker', anonymous=True)
       srv = rospy.Service('/people_detection', People_detection, srv_clbk)      
       rospy.spin()