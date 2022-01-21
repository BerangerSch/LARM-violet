
## Groupe-Violet

- Beranger Scherpereel
- Houssam Ouederni




## Installation

this project requires the instalation of multiple packages before hand such as :
- opencv_libraries for image processing and object identification algorithims :
```bash
git clone https://github.com/opencv/opencv.git
cd opencv
git checkout 3.4.17
mkdir build
cd build
cmake -D'CMAKE_BUILD_TYPE=RELEASE' ..
make -j8

ls -l bin/opencv_createsamples
```
  - openslam for SLAM algorithims such as Gmapping:
```bash
$ sudo apt install ros-noetic-openslam-gmapping ros-noetic-slam-gmapping
```
    
# CHALLENGE 2 

Introduction :

the idee for this project is mapping the environment ( wether from Rosbag data or directly from laser sensor's feedback) and locating multiple Nuka-cola-cans with the help of object detection algorithims then marking these cans on the rviz map with green rectangles

Object detection algorithims :

for this part we adopted Haar's algorithims and apllied modification on it for more precision , starting by training the algorithims by creating the classifier XML file then modifying the script by adding more conditions to the code to avoid wrong detections such as color identification of the red circle of the logo . 

Determination of the object's 2D position :

this part is also included in the identification script where it determines the X and Y coordinates of the contour's centroid point by a mathemetical equation then stores them in InputCentroids

Depth determination (Z axis) :

this part calculates the distance from the camera to the actual object's centroid by taking a reference picture of the can ( Ref-image) and defining the know distance and width of the object in that photo then using this data in other functions such as :

-cans_data (detect the cans and return the cans width in the pixels values. This cans data function simply takes one argument, which image, returns the cans width in the pixels, which is a requirement for the focal length finder and distance finder function.)

-FocalLengthFinder (This function will return the focal length, which is used to find the distance)

-Distance Finder (The distance finder function will return the distance in the centimeters)

