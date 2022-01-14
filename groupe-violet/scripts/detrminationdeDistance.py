# install opencv "pip install opencv-python"
import cv2
import numpy as np
import os
 
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
  
    distance = (real_cans_width * Focal_Length)/cans_width_in_frame
 
    # return the distance
    return distance
 
 
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
 
# show the reference image
cv2.imshow("ref_image", Ref_image)
 
# initialize the camera object so that we
# can get frame from it
cap = cv2.VideoCapture(0)
 
# looping through frame, incoming from
# camera/video
while True:
 
    # reading the frame from camera
    _, frame = cap.read()
 
    # calling cans_data function to find
    # the width of face(pixels) in the frame
    cans_width_in_frame = cans_data(frame)
 
    # check if the cans is zero then not
    # find the distance
    if cans_width_in_frame != 0:
      
        # finding the distance by calling function
        # Distance distance finder function need
        # these arguments the Focal_Length,
        # Known_width(centimeters),
        # and Known_distance(centimeters)
        Distance = Distance_finder(
            Focal_length_found, Known_width, cans_width_in_frame)
 
        # draw line as background of text
        cv2.line(frame, (30, 30), (230, 30), RED, 32)
        cv2.line(frame, (30, 30), (230, 30), BLACK, 28)
 
        # Drawing Text on the screen
        cv2.putText(
            frame, f"Distance: {round(Distance,2)} CM", (30, 35),
          fonts, 0.6, GREEN, 2)
 
    # show the frame on the screen
    cv2.imshow("frame", frame)
 
    # quit the program if you press 'q' on keyboard
    if cv2.waitKey(1) == ord("q"):
        break
 
# closing the camera
cap.release()
 
# closing the the windows that are opened
cv2.destroyAllWindows()