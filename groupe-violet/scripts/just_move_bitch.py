#!/usr/bin/env python3
import rospy, math, std_msgs.msg, time
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

rospy.init_node('dodge', anonymous=True)

commandPublisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

def main():
    rospy.Subscriber("scan", LaserScan, move)
    rospy.spin()

def move(data):
    cmd = Twist()

    # On enregistre tous les angles dans une liste qui correspondra à la liste de ranges
    angle = data.angle_min
    angles = []
    for a in data.ranges :
        angles.append(angle)
        angle += data.angle_increment
    
    # face correspond à l'angle 0° du robot
    face = int(len(angles)/2)
    quart = int(len(angles)/4)
    huitieme = int(len(angles)/8)

    # On observe un par un tous les lasers dans un certain angle autour du robot pour détecter les objets dans un périmètre de 1
    right = 0
    left = 0
    for b in data.ranges[face - quart - huitieme: face]:
        if b < 1:
            right = right + 1
    
    for c in data.ranges[face: face + quart + huitieme]:
        if c < 1:
            left = left + 1        

    # Si les lasers détecte un obstacle dans un périmètre proche et sur un angle important, le robot tourne
    # on a pris en compte une marge d'erreur des lasers donc on se base sur la largeur de l'angle de détection
    if (right > left) and (right > quart / 3):
        cmd.linear.x = 0
        cmd.angular.z = 1
        commandPublisher.publish(cmd)
    elif (left > right) and (left > quart / 3):
        cmd.linear.x = 0
        cmd.angular.z = -1
        commandPublisher.publish(cmd)
    else:
        cmd.linear.x = 2
        cmd.angular.z = 0
        commandPublisher.publish(cmd)

if __name__ == '__main__':
    main()
