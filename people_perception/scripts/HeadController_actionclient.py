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



if __name__ == "__main__":
        rospy.init_node('headcontrollerclient')
        bridge = CvBridge()
        client = actionlib.SimpleActionClient('/head_controller/point_head_action', control_msgs.msg.PointHeadAction)
    
        client.wait_for_server()
        
        ps=PointStamped()
        ps.header.frame_id = "/base_link"
        
        ps.header.stamp  = rospy.Time.now()
        ps.point.x  = 1
        ps.point.y = 1
        ##arbitrary distance
        ps.point.z = 1  

        goal=PointHeadGoal()  
        goal.pointing_frame ="/xtion_link"
        goal.pointing_axis.x = 1.0
        goal.pointing_axis.y = 0.0
        goal.pointing_axis.z = 0.0
        goal.min_duration = rospy.Duration(1)
        goal.max_velocity = 0.25
        goal.target = ps
        print("there")
        client.send_goal(goal)
        print("sent")
        client.wait_for_result()
        msg = rospy.wait_for_message('/xtion/rgb/image_raw', Image)
        image = bridge.imgmsg_to_cv2(msg, desired_encoding= "bgr8")
        cv2.imwrite("/root/images/got2.jpg", image)
        print("get result")
        print(client.get_result())
        client.cancel_all_goals()
        
