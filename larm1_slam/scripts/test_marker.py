#! /usr/bin/env python
import rospy
import geometry_msgs.msg as geo_msgs

rospy.init_node('bottle', anonymous=True)

rate = rospy.Rate(10)

publisher = rospy.Publisher('/bottle', tuple, queue_size=1)
coord = (200, 120)
while not rospy.is_shutdown():
    publisher.publish(coord)
    rate.sleep()