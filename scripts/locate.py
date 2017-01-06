#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry
import math
from std_msgs.msg import Float64
import tf.transformations


corners = []
corners.append(("one", 4.50 ,1.50));
corners.append(("two", 10.50 ,1.50));
corners.append(("three", 10.50,-5.50));
corners.append(("four", 8.50 ,-8.50));
corners.append(("five", 5.00 ,-11.50));
corners.append(("six", 1.50 ,-8.50));

zones = []
zones.append(("one", 1.5, 4.5, -1, 1.5, 2.5, 4.50 ,1.50))
zones.append(("two", 1.5, 10.5, 1.5, 4.5, 9, 10.50 ,1.50))
zones.append(("three", 10.5, 13, -5.5, 4.5, 10, 10.50,-5.50))
zones.append(("four", 8.5, 13, -8.5, -5.5, 4.5, 8.50 ,-8.50))
# zones.append(("five", 1.5, 4.5, -1, 4.5))
# zones.append(("six", 1.5, 4.5, -1, 4.5))




def distance (x1, y1, x2, y2):
    xd= x1-x2
    yd= y1-y2
    return math.sqrt(xd*xd + yd*yd)

def heading (x1, y1, x2, y2, yaw):
    pub = rospy.Publisher('/ron/joint1_position_controller/command', Float64, queue_size=10)
    xd= x2-x1
    yd= y2-y1
    head = math.atan2(yd,xd)
    pub.publish(head-yaw)
    return head


def callback(msg):
    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y
    quaternion1 = (
    msg.pose.pose.orientation.x,
    msg.pose.pose.orientation.y,
    msg.pose.pose.orientation.z,
    msg.pose.pose.orientation.w)
    euler = tf.transformations.euler_from_quaternion(quaternion1)
    yaw = euler[2]
    # rospy.loginfo('x: {}, y: {}'.format(x,y))
    closest_name = None
    closest_distance = None
    for c_name, c_x, c_y in corners:
        dist = distance (x,y, c_x, c_y)
        if closest_distance is None or dist < closest_distance:
            closest_name=c_name
            closest_distance = dist


    curr_name= None
    curr_length= None
    for z_name, x1, x2, y1, y2, z_length,c1, c2 in zones:
        if x>=x1 and x<x2 and y>=y1 and y<y2:
            curr_name= z_name
            curr_length = z_length
            rospy.loginfo('current: {}, length: {}'.format(curr_name, curr_length))
            head = heading (x,y,c1, c2, yaw)




def main():
    rospy.init_node('location_monitor')
    rospy.Subscriber("/ron/odom_diffdrive", Odometry, callback)

    rospy.spin() #loop runs forever

if __name__== '__main__':
    main()
