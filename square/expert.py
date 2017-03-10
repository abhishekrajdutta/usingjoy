#!/usr/bin/env python

import rospy
import actionlib
from nav_msgs.msg import Odometry
import numpy as np
from move_base_msgs.msg import *
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Float64
import tf.transformations
global flag
flag=0
count = 0
# from actionlib_msgs.msg import 

goals = []
# goals.append(("one", -3.426, -3.824, 0.000, 0.000, 0.000, 0.848, 0.529));
goals.append(("one", -4.0, 0.0, 0.000, 0.000, 0.000, 0.707, 0.707));
# goals.append(("three", -3.194, 3.686, 0.000, 0.000, 0.000, 0.232, 0.973));
goals.append(("two", 0.0, 4.0, 0.000, 0.000, 0.000, 0.0 , 1.000));
# goals.append(("five", 3.414, 3.695, 0.000, 0.000, 0.000, -0.526, 0.850));
goals.append(("three", 4.0, 0.0, 0.000, 0.000, 0.000, -0.707, 0.707));
# goals.append(("seven", 3.693, -2.988, 0.000, 0.000, 0.000, 0.929, -0.369));
goals.append(("four", 0.0, -4.0, 0.000, 0.000, 0.000, 1.000, -0.000));

corners = []
corners.append(("one", -2.50 ,2.50));
corners.append(("two", 2.50 ,2.50));
corners.append(("three", 2.50 ,-2.50));
corners.append(("four", -2.50 ,-2.50));




def callback(msg):
	global count, goals

	if msg.status.text == "Goal reached.":
		rospy.loginfo('yay')
		count+=1;
		
	sendgoal(count%4)
		
def sendgoal(count):
	
	pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=10, latch=True)
	global goals,flag
	goal=PoseStamped()
	goal.header.stamp = rospy.get_rostime()
	goal.header.frame_id= "map"
	goal.pose.position.x=goals[count][1]
	goal.pose.position.y=goals[count][2]
	goal.pose.position.z=0.00
	
	goal.pose.orientation.x=0.00
	goal.pose.orientation.y=0.00
	goal.pose.orientation.z=goals[count][6]		
	goal.pose.orientation.w=goals[count][7]
	
	goal.header.seq=count
	pub.publish(goal)
	rospy.loginfo(goal)
	rospy.loginfo(count)
	flag=0

def odom_callback(msg):
	global count
	pub = rospy.Publisher('/ron/joint1_position_controller/commandss', Float64, queue_size=10)
	distance = dist(count%4,msg.pose.pose.position.x,msg.pose.pose.position.y)
	quaternion1 = (msg.pose.pose.orientation.x,msg.pose.pose.orientation.y, msg.pose.pose.orientation.z,msg.pose.pose.orientation.w)
	euler = tf.transformations.euler_from_quaternion(quaternion1)
	yaw = euler[2]
	head=corner(distance, msg.pose.pose.position.x, msg.pose.pose.position.y, yaw)
	pub.publish(head)

def dist(count,x,y):	
	if (corners[count][1]/corners[count][2]) >= 0:
		dist = corners[count][1]-x
	else:
		dist = corners[count][2]-y
	rospy.loginfo(np.absolute(dist))
	return np.absolute(dist)


def corner(distance,x, y, yaw):
	global flag
	if distance<=0.1:
		flag=1
	if flag == 0:
		head = (2.5-distance)/2.5*np.arctan2(x,y)-yaw
	if flag == 1:
		head=0
	return head



def main():
	global count
	count=0
	rospy.init_node('driver_node') 
	rospy.Subscriber("/move_base/result", MoveBaseActionResult, callback)
	rospy.Subscriber('/ron/odom_diffdrive',Odometry,odom_callback)
	sendgoal(count)
	rospy.spin()

if __name__== '__main__':
    main()
