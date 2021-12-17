#!/usr/bin/python3
import math, rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
cmd=Twist()
# Suscribe laser:
rospy.init_node('laser_scan',anonymous=True)

# Initialize ROS::node
commandPublisher = rospy.Publisher(
    '/cmd_vel_mux/input/navi',
    Twist, queue_size=10
)

def move_command(data):
    # Compute cmd_vel here and publish... (do not forget to reduce timer duration)
    global cmd
    cmd.linear.x= 0.1
    cmd.angular.z= 0.0
    if data.ranges[360] > 0.5:
      cmd.linear.x = 0.1
      cmd.angular.z = 0.0
    else :
        cmd.linear.x = 0
        rospy.Timer(rospy.Duration(2), turn(data), oneshot=True)



    commandPublisher.publish(cmd)
    
    rospy.Subscriber('/scan', LaserScan, move_command)

def turn(data):
    global cmd
    cmd.angular.z =0.2
    commandPublisher.publish(cmd)

# call the move_command at a regular frequency:
rospy.Timer( rospy.Duration(0.1), turn(), oneshot=False )

# spin() enter the program in a infinite loop
print("Start move.py")
rospy.spin()



# Publish velocity commandes:
