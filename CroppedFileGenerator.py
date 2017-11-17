#if this doesn't import reinstall python probably / install proper libraries
import numpy as np
import cv2
from matplotlib import pyplot as plt

#Kernel for dilation. Can fiddle with it but doesn't really seem to affect end result much
kernel = np.ones((4,4),np.uint8)

img = cv2.imread('C:\Users\peter\Documents\TestImages\pic99.jpg') #pulls image



imgB = cv2.medianBlur(img,5) #works okay btw res2 is the one that goes down
imgB = cv2.morphologyEx(imgB,cv2.MORPH_OPEN,kernel)

res2 = imgB

cv2.imwrite('C:\Users\peter\Documents\TestImages\Attempts\BlurResult.jpg',res2)


#This stuff works, don't modify anything other than maybe the Canny parameters.
#Canny-on-color works very well. Try other values for science. Will have to adjust for general use
res2 = cv2.Canny(res2,150,350,True)
cv2.imwrite('C:\Users\peter\Documents\TestImages\Attempts\CannyContours.jpg',img)

#Dilates to enhance contours, TWICE, otherwise the contour-finder doesn't find them
img2 = cv2.dilate(res2,kernel,iterations = 2)


#Creates contours
img2, contours, hierarchy = cv2.findContours(img2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
img3 = cv2.drawContours(img2, contours, -1, (0,255,0),3)


img4 = img3
img4 = cv2.cvtColor(img4,cv2.COLOR_GRAY2BGR)
counter = 0
goodshapes = []
#Iterates through contour list and creates files with cropped images.
for num in range(0,len(contours)):
    #mandatory filter or else runtime error
    if len(contours[num]) > 4:
        ellipse = cv2.fitEllipse(contours[num])
        #size based filtering,eventually update to incorporate altitude pixel - inch ratio in order to prevent objects that are way too small from getting caught
        if ellipse[1][0]+ ellipse[1][1] > 80:
            if ellipse[1][0]+ ellipse[1][1] < 300:
                #a good filter for very long and eccentric things. Reduce value in order to mandate even more circular objects
                if (abs(ellipse[1][0] - ellipse[1][1]))/(ellipse[1][0] + ellipse[1][1]) < .4:   
                    area = cv2.contourArea(contours[num])
                    hull = cv2.convexHull(contours[num])
                    hull_area = cv2.contourArea(hull)
                    solidity = float(area)/hull_area
                    #some really squiggly shapes won't be accepted, unfortunately not a catch em all type filter
                    if (solidity > .7):
                        counter = counter + 1
                        #cv2.drawContours(img4,[cv2.convexHull(contours[num])],-1, (0,100, 100),3)
                        img4 = cv2.ellipse(img4,ellipse,(0,255,0),2)
                        #this crops or your image. min max functions prevent out of bounds errors!
                        cropped = res2[max(0,ellipse[0][1]-70):min(ellipse[0][1]+70,5232),max(0,ellipse[0][0]-70):min(ellipse[0][0]+70,3488)]
                        oldCropped = img[max(0,ellipse[0][1]-70):min(ellipse[0][1]+70,5232),max(0,ellipse[0][0]-70):min(ellipse[0][0]+70,3488)]    
                        cropped2 = cv2.dilate(cropped,kernel,iterations = 2)
                        croppednew, tempconts, hierarchtemp = cv2.findContours(cropped2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                        cv2.imwrite('C:\Users\peter\Documents\TestImages\Attempts\RegionsOfInterest\Croppednew'+str(counter)+'.jpg',croppednew)

                        #filters out trees basically. if there's a lot of contours in the area, says image is bad. perhaps worth experimenting with different image sizes
                        if (len(tempconts) < 8):
                            goodshapes = goodshapes + [cropped2]
                            cv2.imwrite('C:\Users\peter\Documents\TestImages\Attempts\RegionsOfInterest\RegionOfInterest'+str(counter)+'.jpg',oldCropped)
                    #else:
                        #img4 = cv2.ellipse(img4,ellipse,(0,255,255),2)

ShapeContour = cv2.drawContours(goodshapes[0], contours, -1, (0,255,0),3)


added = cv2.add(ShapeContour,cv2.imread('C:\Users\peter\Documents\TestImages\Attempts\RegionsOfInterest\Comparison.png',0))
cv2.imwrite('C:\Users\peter\Documents\TestImages\Attempts\RegionsOfInterest\Added.jpg',ShapeContour)


                
cv2.imwrite('C:\Users\peter\Documents\TestImages\Attempts\RotatedFitEllipse.jpg',img4)
print len(goodshapes)




