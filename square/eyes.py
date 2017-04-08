#!/usr/bin/env python

import rospy
import actionlib
from nav_msgs.msg import Odometry
import numpy as np
from move_base_msgs.msg import *
from std_msgs.msg import Float64
import tf.transformations
global flag,head,save,store

look =0
flag=0 # decides what state a robot is in around a turn
corner = 0 # decides which goal the robot is currently going to
store = 0 # decides if the robot should store the current heading angle
save=0 # stores the correct heading angle
radius =5 # distance to wall before turning

def cages (angle): #brings angle into -pi to pi
    if angle>np.pi:
        angle=cages(angle-2*np.pi)
    elif angle<=-np.pi:
        angle=cages(angle+2*np.pi)
    return angle


def dist(corner,x,y):
	d=[]
	
	if corner==0:
		d.append(2.7-y)
		d.append(5.3-y)

	elif corner==1:
		d.append(2.7-x)
		d.append(5.3-x)

	elif corner==2:
		d.append(y+2.7)
		d.append(y+5.3)

	elif corner==3:
		d.append(x+2.7)
		d.append(x+5.3)
	
	if d[0]>0:
		d.append(1)
	elif d[0]<=0:
		d.append(0) #d[2] becomes negative after robot crosses the near wall
		d[0]=np.absolute(d[0])
	
	return d

def turner(d,x,y,yaw):
	# look= np.sqrt(4.5*4.5-d[1]*d[1])
	global store,save,look,corner, radius

	if d[1]>radius:
		look=0

	if d[1]<radius and d[2]==1:
		if corner == 0:
			look = (1.57 - yaw) - np.arccos(d[1]/radius)

		if corner == 1:
			look = (0 - yaw) - np.arccos(d[1]/radius)	

		if corner == 2:
			look = (-1.57 - yaw) - np.arccos(d[1]/radius)
			
		if corner == 3:
			look = (-3.14 - yaw) - np.arccos(d[1]/radius)
					
		# rospy.loginfo(look)
		store =1

	if d[2]==0 and store == 1:
		store = 2
		save=look
		save=cages(save)
		# rospy.loginfo(save)
		# rospy.loginfo('save: {}'.format(save))

	if d[2]==0 and store ==2:
		# look = 1*(1.57 - yaw) - save*(1-d[0])
		look= save*(1-d[0])
		# rospy.loginfo(look)
		if look >= 0:
			look = 0
			corner+=1
		
	return look

def odom_callback(msg):
	pub = rospy.Publisher('/ron/joint1_position_controller/command', Float64, queue_size=10)
	
	distance = dist(corner%4,msg.pose.pose.position.x,msg.pose.pose.position.y)
	quaternion1 = (msg.pose.pose.orientation.x,msg.pose.pose.orientation.y, msg.pose.pose.orientation.z,msg.pose.pose.orientation.w)
	euler = tf.transformations.euler_from_quaternion(quaternion1)
	yaw = euler[2]
	heading=turner(distance, msg.pose.pose.position.x, msg.pose.pose.position.y,yaw)
	pub.publish(heading)

def reset_callback(msg):
	corner=0	
	rospy.loginfo(corner)
	
def main():
	global count
	count=0
	rospy.init_node('noob_node') 
	# rospy.Subscriber("/move_base/result", MoveBaseActionResult, callback)
	rospy.Subscriber('/ron/odom_diffdrive',Odometry,odom_callback)
	rospy.Subscriber('/ron/joint1_position_controller/reset',Float64,reset_callback)
	rospy.spin()

if __name__== '__main__':
    main()
