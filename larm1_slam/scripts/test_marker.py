#! /usr/bin/env python
import rospy
import geometry_msgs.msg as geo_msgs

rospy.init_node('bottle', anonymous=True)

rate = rospy.Rate(10)

publisher = rospy.Publisher('/bottle', geo_msgs.Vector3, queue_size=1)
coord = geo_msgs.Vector3(0, 0, 0.5)
while not rospy.is_shutdown():
    publisher.publish(coord)
    rate.sleep()