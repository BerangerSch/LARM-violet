#!/usr/bin/env python3

from __future__ import print_function

from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
import cv2
import numpy as np
#======================DETECTION PAR ONDELETTES HAAR2============================
import cv2 as cv
import argparse
def detectAndDisplay(frame):
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_gray = cv.equalizeHist(frame_gray)

    #for the color red identification
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0,100,49])
    upper_red = np.array([0,100,100])
    mask = cv2.inRange(hsv, lower_red, upper_red)

    #for the centroids x and y coordinates
    thresh=cv.threshold(frame_gray,127,255,cv.THRESH_BINARY)
    M=cv.moments(thresh)
    inputCentroids=np.zeros(5)
    for i in range (5):
        cX= int(M["m10"] / M["m00"])
        cY= int(M["m01"] / M["m00"])
        inputCentroids[i]=(cX,cY)    
        print(inputCentroids)
    #-- Detect cans
    cans = cans_cascade.detectMultiScale(frame_gray)
    if    np.sum(mask) > 0:
        for (x,y,w,h) in cans:
            center = (x + w//2, y + h//2)
            frame = cv.ellipse(frame, center, (w//2, h//2), 0, 0, 360, (255, 0, 255), 4)
            faceROI = frame_gray[y:y+h,x:x+w]
            
        cv.imshow('Capture - cans detection', frame)
parser = argparse.ArgumentParser(description='Code for Cascade Classifier tutorial.')
parser.add_argument('--cans_cascade', help='Path to cans cascade.', default='/home/bot/catkin_ws/src/LARM-violet/groupe-violet/data/classifier/cascade.xml')
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
    if frame is None:
        print('--(!) No captured frame -- Break!')
        break
    detectAndDisplay(frame)
    if cv.waitKey(10) == 27:
        break
