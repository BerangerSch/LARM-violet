#! /usr/bin/env python
import rospy
import geometry_msgs.msg as geo_msgs
import std_msgs.msg as std_msgs
from visualization_msgs.msg import Marker

def publish_marker(coord):
    bottle = Marker()
    bottle.header.stamp = rospy.Time.now()
    bottle.ns = 'mybottle'
    bottle.type = Marker.CUBE
    bottle.action = Marker.ADD
    bottle.pose.position = coord
    bottle.scale = geo_msgs.Vector3(1, 1, 1)
    bottle.color = std_msgs.ColorRGBA(0, 255, 0, 255)
    print(bottle)

    while not rospy.is_shutdown():
        publisher = rospy.Publisher('/marker', Marker, queue_size=1)
        publisher.publish(bottle)
        rate.sleep()

if __name__ == '__main__':
    rospy.init_node('marker')
    rate = rospy.Rate(10)

    rospy.Subscriber('bottle', geo_msgs.Vector3, publish_marker)
    rospy.spin()
    