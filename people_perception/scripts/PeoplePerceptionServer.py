#!/usr/bin/env python
from os import stat_result
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
from control_msgs.msg import FollowJointTrajectoryAction, FollowJointTrajectoryGoal
import control_msgs.msg 
from trajectory_msgs.msg import JointTrajectoryPoint
from sciroc_navigation.srv import GoToPOI 


client=None
_as=None
state=1
counter=0
go_to_poi=None


def crop(image):
       global state
       th1=rospy.get_param("th1")
       th2=rospy.get_param("th2")
       height, width, _ = image.shape
      
       if state==1:
              image=image[0:width, th1:height-th1]
       elif state==2:
              image=image[0:width, 0:height-th2]
       else:
              image=image[0:width, th2:height] 
       return image

def  navigation(table):
    global state
    if state==1:
         poi_=table+"_people1"
    elif state==2:
         poi_=table+"_people2"
    else:
         poi_=table

    rospy.wait_for_service('go_to_poi_service')

    try:
		
	    go_to_poi = rospy.ServiceProxy('go_to_poi_service', GoToPOI)
	    result = go_to_poi(poi_)

	    if (result.result == 'goal reached'):
		    print (result.result )
	    else: 
		    print ('Point of interest [{poi}] does not exist').format(poi=poi_)
    except rospy.ServiceException as e:
	    print ('Service call failed: {e}'.format(e=e))

def image_acquisition():
      
       global counter
       global state
       
       
       #read and convert image
       bridge = CvBridge()
       #read 5 frames for 3 angulation
       detected_people=[0, 0, 0]
       for i in range(1,4):
              #cambiare topic?
              
              msg = rospy.wait_for_message('/xtion/rgb/image_raw', Image)
              image = bridge.imgmsg_to_cv2(msg, desired_encoding= "bgr8")
             
              #image=crop(image)
              s="/root/images/I.jpg"
              cv2.imwrite(s, image)        
              child_program = subprocess.Popen("/root/images/PeopleDetection.py",1,
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   )
              
              detected_people[i-1]= int(child_program.communicate()[0])
       
       moda=max(set(detected_people),key=detected_people.count)
       

       if moda>2:
             moda=2

       counter=counter+moda
       
       
       

def change_state(new_state):
      global state 
      global client
      
      if new_state==2 or new_state==3:
            angle2=-0.3
            angle1=0.0
        
      else:
            angle1=0.0
            angle2=0.0

      client.wait_for_server()
      G=FollowJointTrajectoryGoal()
       
      G.trajectory.joint_names.append("head_1_joint")
      G.trajectory.joint_names.append("head_2_joint")

      msg=JointTrajectoryPoint()
      G.trajectory.points.append(msg)

      G.trajectory.points[0].positions.append(angle1)
      G.trajectory.points[0].positions.append(angle2)
       
      G.trajectory.points[0].velocities.append(0.01)
      G.trajectory.points[0].velocities.append(0.01)
      G.trajectory.points[0].time_from_start=rospy.Duration(2)
      G.trajectory.header.stamp =rospy.Duration(2)+rospy.Time.now()
      client.send_goal(G)
      client.wait_for_result()
      
      
      state=new_state
      


               

def action_clbk(req):
       global _as, client,state,counter
       state=1
       counter=0
       _res = people_perception.msg.PeopleCounter2Result()
       while True:
              if state==1:
                  
                  navigation(req.table_poi)
                  change_state(2)
              elif state==2:
                  
                  image_acquisition()
                  navigation(req.table_poi)
                  change_state(3)
              elif state==3:
                 
                  image_acquisition()
                  navigation(req.table_poi)
                  change_state(4)
              else:
                  print("DONE")
                  break

       _res.n_people =counter
       print("detected people:")
       print(counter)
       _as.set_succeeded(_res) 
      
    

if __name__ == '__main__':

       rospy.init_node('talker', anonymous=True)
       _as = actionlib.SimpleActionServer('people_detection', people_perception.msg.PeopleCounter2Action,execute_cb=action_clbk, auto_start=False) 
       _as.start() 
       client = actionlib.SimpleActionClient('/head_controller/follow_joint_trajectory', control_msgs.msg.FollowJointTrajectoryAction) 
       go_to_poi = rospy.ServiceProxy('go_to_poi_service', GoToPOI)
       rospy.spin()
