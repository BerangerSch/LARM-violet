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
<<<<<<< HEAD
        while data.ranges[360]< 0.5:
         cmd.linear.x = 0
         cmd.angular.z =0.2
    



=======
        cmd.linear.x = 0
        rospy.Timer(rospy.Duration(2), turn(data), oneshot=True)



    commandPublisher.publish(cmd)
    
    rospy.Subscriber('/scan', LaserScan, move_command)

def turn(data):
    global cmd
    cmd.angular.z =0.2
>>>>>>> 24a8694628a28440438359414edaa6cf611b6eb2
    commandPublisher.publish(cmd)
    
    rospy.Subscriber('/scan', LaserScan, move_command)



# call the move_command at a regular frequency:
<<<<<<< HEAD
rospy.Timer( rospy.Duration(0.1), move_command(), oneshot=False )
=======
rospy.Timer( rospy.Duration(0.1), turn(), oneshot=False )
>>>>>>> 24a8694628a28440438359414edaa6cf611b6eb2

# spin() enter the program in a infinite loop
print("Start move.py")
rospy.spin()



# Publish velocity commandes:
