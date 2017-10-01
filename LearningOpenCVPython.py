import numpy as np
import cv2

img = cv2.imread('C:\Users\peter\Documents\Picturos\Test2.jpg',0)
cv2.imshow('image',img)
k = cv2.waitKey(0)
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()
elif k == ord('s'): # wait for 's' key to save and exit
    cv2.imwrite('C:\Users\peter\Documents\Picturos\TestGray.png',img)
    cv2.destroyAllWindows()
