# SciRoc Challenge: People Perception 

This package is meant to perform **PeoplePerception** behaviour when the *Tiago* robot reaches a table's waypoint, in order to count how many people are seated there 

## launch file
After having launched the simulated environment provided by the SciRoc organizers, this package can be tested through a **launch file** present in the respective directory

## Peopledetection_actionserver.py
Within this [script](https://github.com/AliceNardelli/images/blob/environment/people_perception/scripts/PeopleDetection_actionserver.py), we have defined an action server and an action client. The server implements the people perception action utilising the [PeopleCounter.action](https://github.com/AliceNardelli/images/blob/environment/people_perception/action/PeopleCounter.action)  message reported below: 


```

---
int64 n_people
---
```
Once the people perception action gets activated, the node works as a FSM moving to different head orientations in order to detect accurately the number of people at a certain table. For the sake of completness, the actual node employed for processing the images consists in a non-ROS module called aside as a child process (namely `/root/images/PeopleDetection.py` )by the action server itself (This is due to the fact that ros melodic distro  only supports python 2.7 whereas the people perception library we use needs a newer version).
As far as the client is concerned, it calls the action for controlling the robot's head needed for transitioning between states. Moreover, it exploits the control_msgs/FollowJointTrajectoryAction.msg 

## People Detection_actionclient.py
This node implements a client for calling the people detection action by simply sending a requests and waiting for a response to then print it. This script is needed to allow the use of the action but of course the actual action client will be implemented in the main logic of the robot 

## HeadController_actionclient.py
This node implements the same action client present within the [Peopledetection_actionserver.py](https://github.com/AliceNardelli/images/blob/environment/people_perception/scripts/PeopleDetection_actionserver.py) 

## Images

All the images present within this repo are meant for testing purposes 