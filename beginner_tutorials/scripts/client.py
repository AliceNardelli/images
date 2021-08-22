#!/usr/bin/env python
   
import sys
import rospy
from beginner_tutorials.srv import People_detection


if __name__ == "__main__":
        rospy.init_node('client')
        srv_client= rospy.ServiceProxy('/people_detection', People_detection)
        resp = srv_client()
        print(resp)
