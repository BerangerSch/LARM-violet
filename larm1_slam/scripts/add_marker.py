#! /usr/bin/env python
import rospy
import geometry_msgs.msg as geo_msgs
from geometry_msgs.msg import Pose
import std_msgs.msg as std_msgs
from visualization_msgs.msg import Marker, MarkerArray
import math

def calcul_coord(data):
    x = data.position.x
    depth = data.position.y
    angle = 43.5*(x-640)/640
    x = math.cos(angle)*depth
    y = math.sin(angle)*depth
    return x, y

def publish_markers(img):
    x, y = calcul_coord(img)
    bottle = Marker()
    bottle.header.frame_id = "base_footprint"
    bottle.header.stamp = rospy.Time.now()
    bottle.ns = 'mybottle'
    bottle.type = Marker.CUBE
    bottle.action = Marker.ADD
    bottle.pose.position = geo_msgs.Vector3(x, y, 0.15)
    bottle.scale = geo_msgs.Vector3(0.3, 0.3, 0.3)
    bottle.color = std_msgs.ColorRGBA(0, 255, 0, 255)

    markerArray = MarkerArray()
    python_marker_array = []
    marker_id = 0
    if len(python_marker_array)==0:
        print(bottle)
        bottle.id = marker_id
        python_marker_array.append(bottle)
        markerArray.markers.append(bottle)

    print("\n new : \n", bottle)
    #for i, m in enumerate(python_marker_array):
    python_marker_array.append(bottle)
    markerArray.markers.append(bottle)
    for bottle in markerArray.markers:
        marker_id += 1
        bottle.id = marker_id

    while not rospy.is_shutdown():
        publisher = rospy.Publisher('/marker', MarkerArray, queue_size=1)
        
        publisher.publish(markerArray)
        


rospy.init_node('marker')
rospy.Subscriber('bottle', Pose, publish_markers)
rospy.spin()