import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('C:\Users\peter\Documents\TestImages\pic66.jpg') #pulls image
img = img[0:1000,4000:5000] 

Z = img.reshape((-1,3))
Z = np.float32(Z)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10,1.0)
K = 11
ret, label, center = cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
center = np.uint8(center)
res = center [label.flatten()]
res2 = res.reshape((img.shape))

res2 = cv2.medianBlur(res2,5)
cv2.imwrite('C:\Users\peter\Documents\TestImages\Blur.jpg',res2)
print('done')
