#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry
import math
from std_msgs.msg import Float64
import tf.transformations
global lastc, lastr,lastx,lasty,one,zone1,zone2,head,lasth
head=0
lastc=0
lastr=0
lasth=0 #this is a constant that saves camera heading in the global frame
lastx=0
lasty=0

zone1=0
zone2=0

corners = []
corners.append(("one", 1.50 ,-1.50));
corners.append(("two", -1.50 ,1.50));
zones = []
zones.append(("one", 1.5, 4.5, -1, 1.5, 2.5, 4.50 ,1.50))
zones.append(("two", 1.5, 10.5, 1.5, 4.5, 9, 10.50 ,1.50))
zones.append(("three", 10.5, 13, -5.5, 4.5, 10, 10.50,-5.50))
zones.append(("four", 8.5, 13, -8.5, -5.5, 4.5, 8.50 ,-8.50))




def distance (x1, y1, x2, y2):
    xd= x1-x2
    yd= y1-y2
    return math.sqrt(xd*xd + yd*yd)

def cages (angle): #brings angle into -pi to pi
    if angle>math.pi:
        angle=cages(angle-2*math.pi)
    elif angle<=-math.pi:
        angle=cages(angle+2*math.pi)
    return angle


def cornering (x1, y1, yaw, x2, y2,):
    global zone1,zone2,lastc,lastr,lastx,lasty,head
    if zone1!=zone2:
        lastc=head
        lastr=yaw
    xd= x2-x1
    yd= y2-y1
    head = math.atan2(yd,xd)-yaw
    # rospy.loginfo('head: {}'.format(head))
    head=cages(head)
    return head

def approach (x1, y1, yaw, x2, y2,):
    global zone1,zone2,lastc,lastr,lastx,lasty,head
    if zone1!=zone2:
        lastc=head
        lastr=yaw
    xd= x2-x1
    yd= y2-y1
    head = (1.5-y1)/3*(math.atan2(yd,xd)-yaw)
    head=cages(head)
    rospy.loginfo('lastc: {}'.format(lastc))
    return head

def straight(yaw):
    global zone1,zone2,lastc,lastr,lastx,lasty,head
    if zone1!=zone2:
        lastc=head
        lastr=yaw
    head=1.57-yaw
    head=cages(head)
    return head

def zero(yaw):
    global zone1,zone2,lastc,lastr,lastx,lasty,head
    if zone1!=zone2:
        lastc=head
        lastr=yaw
    head =0
    return head

def nzero(yaw):
    global zone1,zone2,lastc,lastr,lastx,lasty,head,lasth
    if zone1!=zone2:
        lastc=head
        lastr=yaw
        lasth=head+yaw
    head=lasth-yaw
    head=cages(head)
    rospy.loginfo('lastc: {}'.format(lastc))
    # rospy.loginfo('lastc: {}, zone1: {}, zone2: {}'.format(lastc,zone1,zone2))
    return head

def afteru(x,y,yaw):
    global zone1,zone2,lastc,lastr,lastx,lasty,lasth,head
    if zone1!=zone2:
        lastc=head
        lastr=yaw
        lasth=head+yaw
        lastx=x
        lasty=y

    head = lasth-yaw
    head=cages(head)

    head = head*(y-(-1))/(lasty-(-1))

    rospy.loginfo('lastc: {}'.format(lastc))
    return head


def callback(msg):
    global zone1,zone2,head
    pub = rospy.Publisher('/ron/joint1_position_controller/command', Float64, queue_size=10)
    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y
    quaternion1 = (
    msg.pose.pose.orientation.x,
    msg.pose.pose.orientation.y,
    msg.pose.pose.orientation.z,
    msg.pose.pose.orientation.w)
    euler = tf.transformations.euler_from_quaternion(quaternion1)
    yaw = euler[2]
    # rospy.loginfo('yaw: {}'.format(yaw))
    if x>1.5:
        if y>1.5:
            zone1=1
            head = zero(yaw)
            zone2=1

        elif y<=1.5 and y>-1.5:
        #start turning
            zone1=2
            head = approach (x,y,yaw,1.50 ,-1.75)
            zone2=2

        elif y<=-1.5:
            zone1=3
            head = nzero(yaw)
            zone2=3

    elif x<=1.5 and x>-1.5:
        if y<=-1:
            zone1=4
            head=afteru(x,y,yaw)
            zone2=4

    pub.publish(head)


def main():
    rospy.init_node('location_monitor')
    rospy.Subscriber("/ron/odom_diffdrive", Odometry, callback)

    rospy.spin() #loop runs forever

if __name__== '__main__':
    main()
