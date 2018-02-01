import numpy as np
import cv2
from matplotlib import pyplot as plt


Base  = cv2.imread('C:\Users\peter\Documents\TestImages\RegionsOfInterest\Octagon.tif') #pulls image 
Base = cv2.resize(Base,(100,100), interpolation = cv2.INTER_AREA)
cv2.imwrite('C:\Users\peter\Documents\TestImages\RegionsOfInterest\OctagonShrunk.jpg',Base)

