#!/usr/bin/env python
   
import sys
import rospy
import actionlib
from people_perception.msg import PeopleCounter2Action
import people_perception.msg


if __name__ == "__main__":
        rospy.init_node('client')
        client = actionlib.SimpleActionClient('people_detection', PeopleCounter2Action)
        client.wait_for_server()
        goal = people_perception.msg.PeopleCounter2Goal()
        goal.table_poi="t1"
        client.send_goal(goal)
        client.wait_for_result()
        resp=client.get_result()
        print(resp)