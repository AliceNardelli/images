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

client=None
_as=None
state=1
counter=0


def image_acquisition():
       global counter
       global state
       print("IMAGE A")
       print(state)
       
       #read and convert image
       bridge = CvBridge()
       #read 5 frames for 3 angulation
       for i in range(1,3):
              msg = rospy.wait_for_message('/xtion/rgb/image_raw', Image)
              image = bridge.imgmsg_to_cv2(msg, desired_encoding= "bgr8")
              s="/root/images/I"+str(i)+".jpg"
              cv2.imwrite(s, image)
              rospy.sleep(1)
       child_program = subprocess.Popen("/root/images/PeopleDetection.py",
                                 shell=True,
                                 stdout=subprocess.PIPE,
                                 )
       
       detected_people = child_program.communicate()
       print(detected_people[0]) 
       counter=counter+int(detected_people[0])
       
       
       

def change_state(new_state):
      global state 
      global client
      
      if new_state==1 or new_state==4:
             angle1=0.0
             angle2=0.0
      elif new_state==2:
             angle1=0.6
             angle2=0.0 
      else:
             angle1=-0.6
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
      print("head moved")
      
      state=new_state
      print(state)


               

def action_clbk(req):
       global _as, client,state,counter
       state=1
       counter=0
       _res = people_perception.msg.PeopleCounterResult()
       while True:
              if state==1:
                  image_acquisition()
                  change_state(2)
              elif state==2:
                  image_acquisition()
                  change_state(3)
              elif state==3:
                  image_acquisition()
                  change_state(4)
              else:
                  print("DONE")
                  break

       _res.n_people =counter
       _as.set_succeeded(_res) 
      
    

if __name__ == '__main__':

       rospy.init_node('talker', anonymous=True)
       _as = actionlib.SimpleActionServer('people_detection', people_perception.msg.PeopleCounterAction,execute_cb=action_clbk, auto_start=False) 
       _as.start() 

       client = actionlib.SimpleActionClient('/head_controller/follow_joint_trajectory', control_msgs.msg.FollowJointTrajectoryAction) 
       rospy.spin()