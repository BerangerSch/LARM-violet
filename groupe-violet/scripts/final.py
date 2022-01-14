#!/usr/bin/env python3

from __future__ import print_function

from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
import cv2
import numpy as np
import os
#======================DETECTION PAR ONDELETTES HAAR2============================
import cv2 as cv
import argparse

# distance from camera to object(face) measured
# centimeter
Known_distance = 35
 
# width of cans in the real world or Object Plane
# centimeter
Known_width = 7.8
GREEN= ( 0, 255 , 0 )
RED= (0, 0, 255 )
WHITE = (255, 255, 255)
BLACK = (0, 0 , 0)
#definir les fonts
fonts = cv2.FONT_HERSHEY_COMPLEX
 
# cans detector object
cans_detector = cv2.CascadeClassifier("/home/bot/catkin_ws/src/LARM-violet/groupe-violet/data/classifier2/cascade.xml")
 
# focal length finder function
def Focal_Length_Finder(measured_distance, real_width, width_in_Ref_image):
 
    # finding the focal length
    focal_length = (width_in_Ref_image * measured_distance) / real_width
    return focal_length
 
# distance estimation function
def Distance_finder(Focal_Length, real_cans_width, cans_width_in_frame):
    if cans_width_in_frame != 0:
        distance = (real_cans_width * Focal_Length)/cans_width_in_frame
        return distance # return the distance
    else:
        distance = 0
        
 
 
def cans_data(image):
 
    cans_width = 0  # making cans width to zero
 
    print(type(image))
    # converting color image ot gray scale image
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # detecting cans in the image
    cans = cans_detector.detectMultiScale(gray_image, 1.3, 5)

    # looping through the faces detect in the image
    # getting coordinates x, y , width and height
    for (x, y, h, w) in cans:
 
        # draw the rectangle on the cans
        cv2.rectangle(image, (x, y), (x+w, y+h), GREEN, 2)
 
        # getting cans width in the pixels
        cans_width = w
 
    # return the cans width in pixel
    return cans_width
 
 
# reading reference_image from directory
path = '/home/bot/catkin_ws/src/LARM-violet/groupe-violet/data/Ref_image.jpg'
print(os.path.exists(path))
Ref_image = cv2.imread(path)
print(type(Ref_image))
# find the cans width(pixels) in the reference_image
Ref_image_cans_width = cans_data(Ref_image)
 
# get the focal by calling "Focal_Length_Finder"
# cans width in reference(pixels),
# Known_distance(centimeters),
# known_width(centimeters)
Focal_length_found = Focal_Length_Finder(
    Known_distance, Known_width, Ref_image_cans_width)
 
print(Focal_length_found)

def detectAndDisplay(frame):
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_gray = cv.equalizeHist(frame_gray)

    #for the color red identification
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0,100,49])
    upper_red = np.array([0,100,100])
    mask = cv2.inRange(hsv, lower_red, upper_red)

    #for the centroids x and y coordinates detection
    M=cv.moments(mask)
    inputCentroids=np.zeros((5,2))
    for i in range (5):
        if M["m00"] != 0:
            cX= int(M["m10"] / M["m00"])
            cY= int(M["m01"] / M["m00"])
            inputCentroids[i]=(cX,cY)    
            print(inputCentroids)
        else : cX,cY = 0,0
    #-- Detect cans
    cans = cans_cascade.detectMultiScale(frame_gray)
    if    np.sum(mask) > 0:
        for (x,y,w,h) in cans:
            center = (x + w//2, y + h//2)
            frame = cv.ellipse(frame, center, (w//2, h//2), 0, 0, 360, (255, 0, 255), 4)
            faceROI = frame_gray[y:y+h,x:x+w]
            
        cv.imshow('Capture - cans detection', frame)
parser = argparse.ArgumentParser(description='Code for Cascade Classifier tutorial.')
parser.add_argument('--cans_cascade', help='Path to cans cascade.', default='/home/bot/catkin_ws/src/LARM-violet/groupe-violet/data/classifier2/cascade.xml')
parser.add_argument('--camera', help='Camera divide number.', type=int, default=0)
args = parser.parse_args()
cans_cascade_name = args.cans_cascade
cans_cascade = cv.CascadeClassifier()
#-- 1. Load the cascades
if not cans_cascade.load(cv.samples.findFile(cans_cascade_name)):
    print('--(!)Error loading face cascade')
    exit(0)

camera_device = args.camera
#-- 2. Read the video stream
cap = cv.VideoCapture(camera_device)
if not cap.isOpened:
    print('--(!)Error opening video capture')
    exit(0)
while True:
    ret, frame = cap.read()
     # calling cans_data function to find
    # the width of face(pixels) in the frame
    cans_width_in_frame = cans_data(frame)
    if frame is None:
        print('--(!) No captured frame -- Break!')
        break
    detectAndDisplay(frame)
    # finding the distance by calling function
        # Distance distance finder function need
        # these arguments the Focal_Length,
        # Known_width(centimeters),
        # and Known_distance(centimeters)
    Distance = Distance_finder( Focal_length_found, Known_width, cans_width_in_frame)
    if cv.waitKey(10) == 27:
        break
