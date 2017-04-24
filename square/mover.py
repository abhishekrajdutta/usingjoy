#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry
import numpy as np
from move_base_msgs.msg import *
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Float64
import tf.transformations

start=0
goals = []
goals.append(("one", -3.426, -3.824, 0.000, 0.000, 0.000, 0.848, 0.529));
goals.append(("two", -4, 0.0, 0.000, 0.000, 0.000, 0.707, 0.707));
goals.append(("three", -3.194, 3.686, 0.000, 0.000, 0.000, 0.232, 0.973));
goals.append(("four", 0.0, 4, 0.000, 0.000, 0.000, 0.0 , 1.000));
goals.append(("five", 3.414, 3.695, 0.000, 0.000, 0.000, -0.526, 0.850));
goals.append(("six", 4, 0.0, 0.000, 0.000, 0.000, -0.707, 0.707));
goals.append(("seven", 3.693, -2.988, 0.000, 0.000, 0.000, 0.929, -0.369));
goals.append(("eight", 0.0, -4, 0.000, 0.000, 0.000, 1.000, -0.000));


def odom_callback(msg):
	global start
	x=msg.pose.pose.position.x
	y=msg.pose.pose.position.y

	if start==0:
		start=1
		rospy.loginfo("goal1")
		sendgoal(0)
	elif y>2 and y<2.5 and x>-5.5 and x<-2.7:
		rospy.loginfo("goal2")
		sendgoal(1)
	elif y>2.7 and y<5.5 and x>-1.0 and x<-0.5:
		rospy.loginfo("goal3")
		sendgoal(2)
	elif y>2.7 and y<5.5 and x>2 and x<2.5:
		rospy.loginfo("goal4")
		sendgoal(3)
	elif y>0.5 and y<1 and x>2.7 and x<5.5:
		rospy.loginfo("goal5")
		sendgoal(4)
	elif y>-2.5 and y<-2 and x>2.7 and x<5.5:
		rospy.loginfo("goal6")
		sendgoal(5)
	elif y>-5.5 and y<-2.7 and x>0.5 and x<1:
		rospy.loginfo("goal7")
		sendgoal(6)
	elif y>-5.5 and y<-2.7 and x>-2.5 and x<-2:
		rospy.loginfo("goal8")
		sendgoal(7)
	elif y>-1 and y<-0.5 and x>-5.5 and x<-2.7:
		rospy.loginfo("goal1")
		sendgoal(0)

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
	rospy.init_node('mover_node') 
	# rospy.Subscriber("/move_base/result", MoveBaseActionResult, callback)
	rospy.Subscriber('/ron/odom_diffdrive',Odometry,odom_callback)
	# sendgoal(count)
	rospy.spin()

if __name__== '__main__':
    main()
