# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 15:43:16 2021

@author: Hassan Zekkouri
for more details reference to: https://www.pyimagesearch.com/2021/02/22/opencv-connected-component-labeling-and-analysis/
"""

import cv2
import numpy as np # for filtering

def show(win, img):
    cv2.imshow(win, img)
    cv2.waitKey(-1)

imgPath = "license_plate.png"
connectivity = 8


# Step 1: Load the image
image = cv2.imread(imgPath)
# Step 2: Convert to gray scale
gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# Step 3: Threshold (a sort of segmenting)
thresh_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

#show("Gray image", gray_img)
#show("Thresh image", thresh_img)

# Step 4: Apply the function for connected components (cc)
output = cv2.connectedComponentsWithStats(thresh_img, connectivity, cv2.CV_32S)
(numLabels, labels, stats, centroids) = output
# labels: the labeled image
# stats: bounding box, area, ... of each component
# centroids: (x,y) coordinates of the center of each cc

def basic():
    # Step 5: Parsing the values and visualization
    for i in range(0, numLabels):
        # The first cc is the *background*
        if i == 0:
            text = f"examining component {i+1}/{numLabels}"
        else:
            text = f"examining component {i+1}/{numLabels}"
        # Printing status info
        print("[INFO] {}".format(text))
        
        # Extract the stats of the current cc
        x, y = stats[i, cv2.CC_STAT_LEFT], stats[i, cv2.CC_STAT_TOP]
        w, h = stats[i, cv2.CC_STAT_WIDTH], stats[i, cv2.CC_STAT_HEIGHT]
        area = stats[i, cv2.CC_STAT_AREA]
        cX, cY =  centroids[i]
        
        # clone the image for drawing the bbox surrounding the cc
        # along with a circle corresponding to the center
        output = image.copy()
        cv2.rectangle(output, (x,y), (x+w, y+h), (0, 255, 0), 3)
        cv2.circle(output, (int(cX), int(cY)), 4, (0, 0, 255), -1)
        
        # show("ccmage", output)
        # construct a mask for the current cc by finding
        # a pixel in the labels array that have the current cc ID
        componentMask = (labels == i).astype("uint8") * 255
        # show image and c mask
        cv2.imshow("Output", output)
        cv2.imshow("Connected Component", componentMask)
        cv2.waitKey(0)

def filtering():
    # Second post part: Filtering connected components
    # Step A: Initialize an output mask to store all characters parsed
    # from the license plate
    mask = np.zeros(gray_img.shape, dtype="uint8")
    
    # Step 5: Parsing the values and visualization
    for i in range(1, numLabels):
        text = f"examining component {i+1}/{numLabels}"
        # Printing status info
        print("[INFO] {}".format(text))
        
        # Extract the stats of the current cc
        x, y = stats[i, cv2.CC_STAT_LEFT], stats[i, cv2.CC_STAT_TOP]
        w, h = stats[i, cv2.CC_STAT_WIDTH], stats[i, cv2.CC_STAT_HEIGHT]
        area = stats[i, cv2.CC_STAT_AREA]
        cX, cY =  centroids[i]
        
        # Step B: Manual filtering (depends on the application)
        # ensure the width, height, and area are all neither too small
    	# nor too big
        keepWidth = w > 5 and w < 50
        keepHeight = h > 45 and h < 65
        keepArea = area > 500 and area < 1500
        
        # ensure the cc we are examining passes all
        # three tests
        if all((keepWidth, keepHeight, keepArea)):
            # construct a mask for the current cc and then
            # take the bitwise OR with the mask
            print("[INFO] keeping connected component '{}'".format(i))
            componentMask = (labels == i).astype("uint8") * 255
            mask = cv2.bitwise_or(mask, componentMask)
        
        
    # show("ccmage", output)
    # show image and c mask
    cv2.imshow("Image", image)
    cv2.imshow("Characters", mask)
    cv2.waitKey(0)


 
filtering()

 
    
    
    















