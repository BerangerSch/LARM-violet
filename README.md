
## Groupe-Violet

- Beranger Scherpereel
- Houssam Ouederni

## Remerciement 

We would like to thank our professors for introducing  us to this highly interesting and fun UV and most importantly , thank you for relentlesly answering our sometimes stupid questions over and over again until they got stuck in our brains .

## YouTube introduction video link 

https://youtu.be/WqBGkqlDYac

## Installation

The project requires the instalation of the following packages before hand :

- move_base libraries and local planner :
```bash
sudo apt-get install ros-noetic-move-base

sudo apt-get install ros-noetic-dwa-local-planner
```
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
    
# CHALLENGE 3 

Introduction :

The goal of this project is to develop an autonomus mobile robot that achieves multiple tasks from mapping it's surroundings to autonomously navigate throught 
it towards a preset goal while avoiding obtstacles, identifiying and localising sertant objects (nuka-cola-cans) then placing their location in the R-viz map .

Launch files :
- the detailed description of each launch file is availabe in the launch/READme.md file .

Marking the bottles :

this script receives the 3 coordinates of the bottles (subscribed to the vision node ) then converts thes coordinates to a map position then publishes thes positions in the /marker topic 

Autonomous nagivation :

for this end we have opted to use the move_base pkg wich only requires the modification of few param.yaml for it to function along with the slam Gmapping node 
Object detection algorithims :

Object detection algorithims :

for this part we adopted Haar's algorithims and apllied modification on it for more precision , starting by training the algorithims by creating the classifier XML file then modifying the script by adding more conditions to the code to avoid wrong detections such as color identification of the red circle of the logo . 

Determination of the object's 2D position :

this part is also included in the identification script where it determines the X and Y coordinates of the contour's centroid point by a mathemetical equation then stores them in InputCentroids

Depth determination (Z axis) :

this part calculates the distance from the camera to the actual object's centroid by taking a reference picture of the can ( Ref-image) and defining the know distance and width of the object in that photo then using this data in other functions such as :

-cans_data (detect the cans and return the cans width in the pixels values. This cans data function simply takes one argument, which image, returns the cans width in the pixels, which is a requirement for the focal length finder and distance finder function.)

-FocalLengthFinder (This function will return the focal length, which is used to find the distance)

-Distance Finder (The distance finder function will return the distance in the centimeters)


