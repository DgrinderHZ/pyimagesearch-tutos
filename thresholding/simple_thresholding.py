# import packages
import cv2

# load the image
path = 
image = cv2.imread(path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# remove unecessary high frequency edges
blur = cv2.GaussianBlur(gray, (7, 7), 0)

# threshold (black bg)
(T, threshInv) = cv2.threshold(blur, 200, 255, cv2.THRESH_BINARY_INV)
cv2.imdshow("Threshold binary inverse", threshInv)

# using normal thresholding (white bg)
(T, thresh) = cv2.threshold(blur, 200, 255, cv2.THRESH_BINARY)
cv2.imdshow("Threshold binary inverse", thresh)
