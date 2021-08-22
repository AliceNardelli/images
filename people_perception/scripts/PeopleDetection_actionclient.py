#!/usr/bin/env python
   
import sys
import rospy
import actionlib
from people_perception.msg import PeopleCounterAction
import people_perception.msg


if __name__ == "__main__":
        rospy.init_node('client')
        client = actionlib.SimpleActionClient('people_detection', PeopleCounterAction)
        print(1)
        client.wait_for_server()
        print(2)
        goal = people_perception.msg.PeopleCounterGoal(n_orientations=3)
        print(3)
        client.send_goal(goal)
        print(4)
        client.wait_for_result()
        resp=client.get_result()
        print(resp)
