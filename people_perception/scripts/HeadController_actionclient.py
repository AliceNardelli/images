#!/usr/bin/env python
   
import sys
import rospy
import actionlib
from geometry_msgs.msg import PointStamped
from control_msgs.msg import PointHeadAction
from control_msgs.msg import PointHeadGoal
import control_msgs.msg 
import geometry_msgs.msg
import time
import datetime
from cv_bridge import CvBridge
import cv2 
from sensor_msgs.msg import Image
from control_msgs.msg import FollowJointTrajectoryAction, FollowJointTrajectoryGoal
import control_msgs.msg 
from trajectory_msgs.msg import JointTrajectoryPoint



if __name__ == "__main__":
       rospy.init_node('headcontrollerclient')
       client = actionlib.SimpleActionClient('/head_controller/follow_joint_trajectory', control_msgs.msg.FollowJointTrajectoryAction) 
       client.wait_for_server(rospy.Duration(20))
       print('connected')
       G=FollowJointTrajectoryGoal()
       
       G.trajectory.joint_names.append("head_1_joint")
       G.trajectory.joint_names.append("head_2_joint")
      
    
       msg=JointTrajectoryPoint()
       G.trajectory.points.append(msg)
       print(len(G.trajectory.points))
       G.trajectory.points[0].positions.append(0.6)
       G.trajectory.points[0].positions.append(0.3)
       print(len(G.trajectory.points[0].positions))
       
       G.trajectory.points[0].velocities.append(0.01)
       G.trajectory.points[0].velocities.append(0.01)
       G.trajectory.points[0].time_from_start=rospy.Duration(2)
       G.trajectory.header.stamp =rospy.Duration(2)+rospy.Time.now()
       client.send_goal(G)
       client.wait_for_result()
       print("terminate")
       rospy.spin()

        
