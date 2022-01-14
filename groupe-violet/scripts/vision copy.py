#!/usr/bin/env python3

from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier 
import matplotlib.pyplot as plt
import cv2
import numpy as np

"""
#=====================SEGMENTATION PAR SEUILLAGE=========================================

def souris(event, x, y, flags, param):
    global lo, hi, color, hsv_px
    
    if event == cv2.EVENT_MOUSEMOVE:
        # Conversion des trois couleurs RGB sous la souris en HSV
        px = frame[y,x]
        px_array = np.uint8([[px]])
        hsv_px = cv2.cvtColor(px_array,cv2.COLOR_BGR2HSV)
    
    if event==cv2.EVENT_MBUTTONDBLCLK:
        color=image[y, x][0]

    if event==cv2.EVENT_LBUTTONDOWN:
        if color>5:
            color-=1

    if event==cv2.EVENT_RBUTTONDOWN:
        if color<250:
            color+=1
            
    lo[0]=color-5
    hi[0]=color+5

color=100

lo=np.array([color-5, 100, 50])
hi=np.array([color+5, 255, 255])

color_infos=(0, 0, 255)

cap=cv2.VideoCapture(0)
cv2.namedWindow('Camera')
cv2.setMouseCallback('Camera', souris)
hsv_px = [0,0,0]

while True:
    ret, frame=cap.read()
    image=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    image=cv2.blur(image, (7, 7))
    mask=cv2.inRange(image, lo, hi)
    mask=cv2.erode(mask, None, iterations=4)
    mask=cv2.dilate(mask, None, iterations=4)
    image2=cv2.bitwise_and(frame, frame, mask= mask)
    cv2.putText(frame, "Couleur: {:d}".format(color), (10, 30), cv2.FONT_HERSHEY_DUPLEX, 1, color_infos, 1, cv2.LINE_AA)
    
    # Affichage des composantes HSV sous la souris sur l'image
    pixel_hsv = " ".join(str(values) for values in hsv_px)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, "px HSV: "+pixel_hsv, (10, 260),
               font, 1, (255, 255, 255), 1, cv2.LINE_AA)

    elements=cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    if len(elements) > 0:
        c=max(elements, key=cv2.contourArea)
        ((x, y), rayon)=cv2.minEnclosingCircle(c)
        if rayon>30:
            cv2.circle(image2, (int(x), int(y)), int(rayon), color_infos, 2)
            cv2.circle(frame, (int(x), int(y)), 5, color_infos, 10)
            cv2.line(frame, (int(x), int(y)), (int(x)+150, int(y)), color_infos, 2)
            cv2.putText(frame, "Objet !!!", (int(x)+10, int(y) -10), cv2.FONT_HERSHEY_DUPLEX, 1, color_infos, 1, cv2.LINE_AA)
               
    cv2.imshow('Camera', frame)
    cv2.imshow('image2', image2)
    cv2.imshow('Mask', mask)
    
    if cv2.waitKey(1)&0xFF==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
"""

"""#===========================SEGMENTATION K-MEANS======================================

#Ensuite charger une image et la convertir de BGR à RGB si nécessaire et l’afficher :
image = cv2.imread('lena.jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
plt.figure()
plt.axis("off")
plt.imshow(image)

n_clusters=5
image = image.reshape((image.shape[0] * image.shape[1], 3))
clt = KMeans(n_clusters = n_clusters )
clt.fit(image)

def centroid_histogram(clt):
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    # normalize the histogram, such that it sums to one
    hist = hist.astype("float")
    hist /= hist.sum()

    return hist

def plot_colors(hist, centroids):
    bar = np.zeros((50, 300, 3), dtype="uint8")
    startX = 0

    # loop over the percentage of each cluster and the color of
    # each cluster
    for (percent, color) in zip(hist, centroids):
        # plot the relative percentage of each cluster
        endX = startX + (percent * 300)
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                      color.astype("uint8").tolist(), -1)
        startX = endX

    return bar

hist = centroid_histogram(clt)
bar = plot_colors(hist, clt.cluster_centers_)
plt.figure()
plt.axis("off")
plt.imshow(bar)
plt.show()
"""

"""
#=======================CLASSIFICATION IMAGES METHODE KNN===========================

basedir_data = "../data/"
rel_path = basedir_data + "cifar-10-batches-py/"

#Désérialiser les fichiers image afin de permettre l’accès aux données et aux labels:

def unpickle(file):
    import pickle
    with open(file, 'rb') as fo:
        dict = pickle.load(fo,encoding='bytes')
    return dict

X = unpickle(rel_path + 'data_batch_1')
img_data = X[b'data']
img_label_orig = img_label = X[b'labels']
img_label = np.array(img_label).reshape(-1, 1)

print(img_data)
print('shape', img_data.shape)

print(img_label)
print('shape', img_label.shape)

test_X = unpickle(rel_path + 'test_batch')
test_data = test_X[b'data']
test_label = test_X[b'labels']
test_label = np.array(test_label).reshape(-1, 1)

sample_img_data = img_data[0:10, :]
print(sample_img_data)
print('shape', sample_img_data.shape)
print('shape', sample_img_data[1,:].shape)

one_img=sample_img_data[0,:]
r = one_img[:1024].reshape(32, 32)
g = one_img[1024:2048].reshape(32, 32)
b = one_img[2048:].reshape(32, 32)
rgb = np.dstack([r, g, b])
cv2.imshow('Image CIFAR',rgb)
cv2.waitKey(0)
cv2.destroyAllWindows()

def pred_label_fn(i, original):
    return original + '::' + meta[YPred[i]].decode('utf-8')

nbrs = KNeighborsClassifier(n_neighbors=3, algorithm='brute').fit(img_data, img_label_orig)

# test sur les 10 premières images
data_point_no = 10
sample_test_data = test_data[:data_point_no, :]

YPred = nbrs.predict(sample_test_data)

for i in range(0, len(YPred)):
    show_img(sample_test_data, test_label, meta, i, label_fn=pred_label_fn)
"""

"""#======================DETECTION PAR ONDELETTES HAAR============================

def detectAndDisplay(frame):
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_gray = cv2.equalizeHist(frame_gray)

    #-- Detect cans
    cans = can_cascade.detectMultiScale(frame_gray)
    for (x,y,w,h) in cans:
        center = (x + w//2, y + h//2)
        frame = cv2.ellipse(frame, center, (w//2, h//2), 0, 0, 360, (0, 0, 255), 4)

        faceROI = frame_gray[y:y+h,x:x+w]

    cv2.imshow('Can detection', frame)

can_cascade = cv2.CascadeClassifier()

if not can_cascade.load(cv2.samples.finFile('../data/haarcascades/can_cascade.xml'):
    print('--(!)Error loading eyes cascade')
    exit(0)

while True:
    ret, frame = cap.read()

    detectAndDisplay(frame)

    if cv2.waitKey(1)&0xFF==ord('q'):
        break
cap.release()
cv2.destroyAllWindows() 
"""
#======================DETECTION PAR ONDELETTES HAAR2============================
from __future__ import print_function
import cv2 as cv
import argparse
def detectAndDisplay(frame):
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_gray = cv.equalizeHist(frame_gray)
    #-- Detect faces
    cans = cans_cascade.detectMultiScale(frame_gray)
    for (x,y,w,h) in cans:
        center = (x + w//2, y + h//2)
        frame = cv.ellipse(frame, center, (w//2, h//2), 0, 0, 360, (255, 0, 255), 4)
        faceROI = frame_gray[y:y+h,x:x+w]
        
    cv.imshow('Capture - Face detection', frame)
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