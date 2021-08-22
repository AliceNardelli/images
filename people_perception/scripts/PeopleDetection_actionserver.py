#!/usr/bin/env python
import sys
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image 
import subprocess
import random
import socket, select
from time import gmtime, strftime
from random import randint
from cv_bridge import CvBridge
import cv2 
import actionlib 
import people_perception.msg

def action_clbk(req):
       global _as
       _res = people_perception.msg.PeopleCounterResult()
       #read and convert image
       bridge = CvBridge()
       #read 5 frames for 3 angulation
       print(2)
       #msg = rospy.wait_for_message('/xtion/rgb/image_raw', Image)
       print(2)
       #image = bridge.imgmsg_to_cv2(msg, desired_encoding= "bgr8")
       #cv2.imwrite("/root/images/provaimm.jpg", image)
       child_program = subprocess.Popen("/root/images/PeopleDetection.py",
                                 shell=True,
                                 stdout=subprocess.PIPE,
                                 )
       
       detected_people = child_program.communicate()
       print(detected_people[0]) 
       _res.n_people = int(detected_people[0])
       _as.set_succeeded(_res) 
      
    

if __name__ == '__main__':
       global _as
       rospy.init_node('talker', anonymous=True)
       _as = actionlib.SimpleActionServer('people_detection', people_perception.msg.PeopleCounterAction,execute_cb=action_clbk,auto_start=False) 
       _as.start()   
       rospy.spin()