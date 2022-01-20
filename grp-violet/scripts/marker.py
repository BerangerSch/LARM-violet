#! /usr/bin/env python3
import rospy
import geometry_msgs.msg as geo_msgs
from geometry_msgs.msg import Pose
import std_msgs.msg as std_msgs
from visualization_msgs.msg import Marker
import numpy as np

publisher = rospy.Publisher('/marker', Marker, queue_size=1)

marker_array = []

MIN_BETWEEN_BOTTLES = 0.4   #Minimal distance between two bottles
BOTTLE_RADIUS = 0.4         #Minimal area of each bottle

#Function to obtain the distance between two bottles
def calcul_dist(bottle, marker):
    p1 = np.array([bottle.pose.position.x, bottle.pose.position.y, bottle.pose.position.z])
    p2 = np.array([marker.pose.position.x, marker.pose.position.y, marker.pose.position.z])
    squared_dist = np.sum((p1-p2)**2, axis=0)
    distance = np.sqrt(squared_dist)
    return distance

#Function to publish markers for each bottle detected
def publish_markers(coord):
    x = coord.position.x
    y = coord.position.y
    #Initialization of the marker for a bottle 
    bottle = Marker()
    bottle.header.frame_id = "base_footprint"
    bottle.header.stamp = rospy.Time.now()
    bottle.ns = 'mybottle'
    bottle.id = len(marker_array)
    bottle.type = Marker.CUBE
    bottle.action = Marker.ADD
    bottle.pose.position = geo_msgs.Vector3(x, y, 0.15)
    bottle.scale = geo_msgs.Vector3(0.3, 0.3, 0.3)
    bottle.color = std_msgs.ColorRGBA(0, 255, 0, 255)

    #Publication of the bottle's marker to the topic 
    if len(marker_array)==0:
        marker_array.append(bottle)
        publisher.publish(bottle)
        print(marker_array)
    else:
        distance = calcul_dist(bottle, marker_array[-1])
        if len(marker_array) ==1:
            if distance > MIN_BETWEEN_BOTTLES:
                marker_array.append(bottle)
                publisher.publish(bottle)
        else:
            for i in range(len(marker_array)-1):
                area = calcul_dist(bottle, marker_array[i])
                if distance > MIN_BETWEEN_BOTTLES and area > BOTTLE_RADIUS:
                    if bottle.id != marker_array[-1].id:
                        marker_array.append(bottle)
                        publisher.publish(bottle)
                        print(marker_array)
                    else:
                        break


rospy.init_node('marker')
rospy.Subscriber('bottle', Pose, publish_markers)
rospy.spin()