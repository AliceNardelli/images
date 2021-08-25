#!/usr/bin/env python
   
import sys
import rospy
import actionlib
from people_perception.msg import PeopleCounterAction
import people_perception.msg


if __name__ == "__main__":
        rospy.init_node('client')
        client = actionlib.SimpleActionClient('people_detection', PeopleCounterAction)
        client.wait_for_server()
        goal = people_perception.msg.PeopleCounterGoal()
        client.send_goal(goal)
        client.wait_for_result()
        resp=client.get_result()
        print(resp)
