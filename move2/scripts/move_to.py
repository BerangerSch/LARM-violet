#!/usr/bin/env python3

import rospy, rospy, math, std_msgs.msg, time
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist
import tf

tfListener = tf.TransformListener()
rospy.init_node('listener', anonymous=True)
commandPublisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
def callback(data):
    local_goal= tfListener.transformPose("/base_footprint", data)
    print(data)
    
def main():
    rospy.Subscriber("move_base_simple/goal", PoseStamped, callback)
    commandPublisher.publish(Twist())
    rospy.spin()

if __name__ == '__main__':
    main()