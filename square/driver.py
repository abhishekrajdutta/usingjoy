#!/usr/bin/env python

import rospy
import actionlib
from nav_msgs.msg import Odometry
import numpy as np
from move_base_msgs.msg import *
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Float64
import tf.transformations
global flag,head,save,store
from geometry_msgs.msg import Point32
from geometry_msgs.msg import Polygon


flag=0 # decides what state a robot is in around a turn
count = 0 # decides which goal the robot is currently going to
store = 0 # decides if the robot should store the current heading angle
save=0 # stores the correct heading angle




goals = []
# goals.append(("one", -3.426, -3.824, 0.000, 0.000, 0.000, 0.848, 0.529));
goals.append(("one", -3.9, 0.0, 0.000, 0.000, 0.000, 0.707, 0.707));
# goals.append(("three", -3.194, 3.686, 0.000, 0.000, 0.000, 0.232, 0.973));
goals.append(("two", 0.0, 3.9, 0.000, 0.000, 0.000, 0.0 , 1.000));
# goals.append(("five", 3.414, 3.695, 0.000, 0.000, 0.000, -0.526, 0.850));
goals.append(("three", 3.6, 0.0, 0.000, 0.000, 0.000, -0.707, 0.707));
# goals.append(("seven", 3.693, -2.988, 0.000, 0.000, 0.000, 0.929, -0.369));
goals.append(("four", 0.0, -3.9, 0.000, 0.000, 0.000, 1.000, -0.000));

corners = []
corners.append(("one", -2.50 ,2.50));
corners.append(("two", 2.50 ,2.50));
corners.append(("three", 2.50 ,-2.50));
corners.append(("four", -2.50 ,-2.50));




def callback(msg):
	global count, goals, flag

	if msg.status.text == "Goal reached.":
		# rospy.loginfo('yay')
		count+=1
		flag=1
		
	sendgoal(count%4)


def sendgoal(counter):
	global goals,flag,count
	# dimensions()
	pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=10, latch=True)
	goal=PoseStamped()
	goal.header.stamp = rospy.get_rostime()
	goal.header.frame_id= "map"
	goal.pose.position.x=goals[counter][1]
	goal.pose.position.y=goals[counter][2]
	goal.pose.position.z=0.00
	
	goal.pose.orientation.x=0.00
	goal.pose.orientation.y=0.00 
	goal.pose.orientation.z=goals[counter][6]		
	goal.pose.orientation.w=goals[counter][7]
	
	goal.header.seq=count
	pub.publish(goal)
	# rospy.loginfo(goal)
	# rospy.loginfo(count)
	

def main():
	global count
	count=0
	rospy.init_node('driver_node') 
	rospy.Subscriber("/move_base/result", MoveBaseActionResult, callback)
	# rospy.Subscriber('/ron/odom_diffdrive',Odometry,odom_callback)
	sendgoal(count)
	rospy.spin()

if __name__== '__main__':
    main()
