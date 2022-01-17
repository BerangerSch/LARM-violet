#!/usr/bin/env python3

import rospy, rospy, math, std_msgs.msg, time
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Twist
import tf
from math import atan2
from nav_msgs.msg import Odometry

rospy.init_node('listener', anonymous=True)
tfListener = tf.TransformListener()
commandPublisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

def callback(data):
 
    #( coordonnees de goal pour comparer ensuite l'orientation du robot par rapport au goal)
    #x=data.pose.position.x
    #y=data.pose.position.y
    #rot_q = msg.pose.pose.Quaternion.orientation
    #(roll, pitch, theta) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])
    # angle_to_goal = atan2(y,x)

   #our goal position
    local_goal= tfListener.transformPose("/base_footprint", data)
    print(type(local_goal))
    cmd= Twist()
    #saves all the angles in a list. The list of angles corresponds to the list of ranges
    angle= data.angle_min
    angles= []
    for a in data.ranges :
        angles.append(angle)
        angle+= data.angle_increment
    
    #middle is the angle value for the position directly in front of the robot
    middle = len(angles) / 2
    middle = int(middle)
    quarter = len(angles) / 4
    quarter = int(quarter)
    eigth = len(angles) / 8
    eigth = int(eigth)

    #we count all the individual laser rays in a certain angle left and right of the robot, which report an obstacle closer than 0,4
    right = 0
    left = 0
    for b in data.ranges[middle - quarter - eigth: middle]:
        if b < 0.4:
            right = right + 1
    
    for c in data.ranges[middle: middle + quarter + eigth]:
        if c < 0.4:
            left = left + 1        

    #turn, if most of the sensors in the important angle report an obstacle close by
    #we did this, because the sensor probably picked up some false readings and the robot startet to shake
    #with this solution, some at64false readings don't interrupt a smooth turn
    if (right > left) and (right > quarter / 3):
        cmd.linear.x = 0
        cmd.angular.z= 0.5
        commandPublisher.publish(cmd)
    elif (left > right) and (left > quarter / 3):
        cmd.linear.x= 0
        cmd.angular.z= -0.5
        commandPublisher.publish(cmd)
    elif abs(angle_to_goal - theta) > 0.1:
        cmd.linear.x= 0.0
        cmd.angular.z= 0.3
        commandPublisher.publish(cmd)
    else :
        cmd.linear.x = 0.5
        cmd.angular.z = 0.0     
    print(data)
    
def main():
    rospy.Subscriber("move_base_simple/goal", PoseStamped, callback)

    rospy.spin()

if __name__ == '__main__':
    main()