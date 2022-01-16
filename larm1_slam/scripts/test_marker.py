#! /usr/bin/env python
import rospy
from geometry_msgs.msg import Pose

rospy.init_node('bottle', anonymous=True)

rate = rospy.Rate(10)

publisher = rospy.Publisher('/bottle', Pose, queue_size=1)
p = Pose()
p.position.x = 200 #x
p.position.y = 1 #depth
while not rospy.is_shutdown():
    publisher.publish(p)
    rate.sleep()