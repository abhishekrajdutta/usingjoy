#!/usr/bin/env python

import rospy
import actionlib
from nav_msgs.msg import Odometry
import numpy as np
from move_base_msgs.msg import *

odom = Odometry()
def set_goal(a,b,x,y,z,w):
    goal = MoveBaseSimpleGoal()
    goal.target_pose.pose.position.x = a
    goal.target_pose.pose.position.y = b
    goal.target_pose.pose.orientation.x = x
    goal.target_pose.pose.orientation.y = y
    goal.target_pose.pose.orientation.z = z
    goal.target_pose.pose.orientation.w = w
    goal.target_pose.header.frame_id = 'odom'
    #goal.target_pose.header.child_frame_id = 'base_link'
    goal.target_pose.header.stamp = rospy.Time.now()

    return goal

def set_odom_goal(od,d1,d2):
     goal = MoveBaseGoal()
     goal.target_pose.pose.position.x = od.pose.pose.position.x + d1
     goal.target_pose.pose.position.y = od.pose.pose.position.y + d2
     goal.target_pose.pose.orientation.x = 0
     goal.target_pose.pose.orientation.y = 0
     goal.target_pose.pose.orientation.z = 0
     goal.target_pose.pose.orientation.w = 1

     goal.target_pose.header.frame_id = 'odom'
     #goal.target_pose.header.child_frame_id = 'base_link'
     goal.target_pose.header.stamp = rospy.Time.now()
     return goal

def send_goal(sac,goal):
    #start listner
    sac.wait_for_server()

    #send goal
    sac.send_goal(goal)

    #finish
    sac.wait_for_result()

    #print result
    print sac.get_result()

def odom_callback(msg):
    global odom
    odom=msg

def simple_move():
    global odom
    rospy.init_node('simple_move')

    d1=1
    d2=1
    rospy.Subscriber('/ron/odom_diffdrive',Odometry,odom_callback)
    #Simple Action Client
    sac = actionlib.SimpleActionClient('move_base', MoveBaseAction )

    #create goal
    #goal = MoveBaseGoal()

    #use self?
    #set goal
    #goal.target_pose.pose.position.x = d
    #goal.target_pose.pose.orientation.w = 1.0
    #goal.target_pose.header.frame_id = 'odom'
    #goal.target_pose.header.stamp = rospy.Time.now()


    #send_goal(sac,goal)




    for i in range(1,4):
        g2=set_odom_goal(odom,d1,-d2)
        send_goal(sac,g2)
        rospy.loginfo('goal sent')

        g2=set_odom_goal(odom,d1,d2)
        send_goal(sac,g2)




if __name__ == '__main__':
    try:
        simple_move()
    except rospy.ROSInterruptException:
        print "Keyboard Interrupt"
