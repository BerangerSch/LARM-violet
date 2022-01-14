#! /usr/bin/env python
import rospy
import geometry_msgs.msg as geo_msgs
import std_msgs.msg as std_msgs
from visualization_msgs.msg import Marker
import math

def calcul_coord(data):
    x = data[0]
    depth = data[1]
    angle = 43.5*(x-640)/640
    x = math.cos(angle)*depth
    y = math.sin(angle)*depth
    return x, y



def publish_marker(img):
    x, y = calcul_coord(img)
    bottle = Marker()
    bottle.header.stamp = rospy.Time.now()
    bottle.ns = 'mybottle'
    bottle.type = Marker.CUBE
    bottle.action = Marker.ADD
    bottle.pose.position = geo_msgs.Vector3(x, y, 0.5)
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

    rospy.Subscriber('bottle', tuple, publish_marker)
    rospy.spin()
    