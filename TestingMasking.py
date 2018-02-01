import numpy as np
import cv2
from matplotlib import pyplot as plt
# Load two images
img1 = cv2.imread('C:\Users\peter\Documents\TestImages\RegionsOfInterest\RegionOfInterest1from99.jpg')
img2 = cv2.imread('C:\Users\peter\Documents\TestImages\RegionsOfInterest\BlackWhited.jpg')

# I want to put logo on top-left corner, So I create a ROI

# Now create a mask of logo and create its inverse mask also
img2gray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)

ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)

mask_inv = cv2.bitwise_not(mask)


# Now black-out the area of logo in ROI
img1_bg = cv2.bitwise_and(img1,img1,mask = mask)
cv2.imshow('res',img1_bg)


#cv2.imshow('res',img1)
cv2.waitKey(0)
cv2.destroyAllWindows()
