#if this doesn't import reinstall python probably / install proper libraries
import numpy as np
import cv2
from matplotlib import pyplot as plt

#Kernel for dilation. Can fiddle with it but doesn't really seem to affect end result much
kernel = np.ones((4,4),np.uint8)

# List of good files: 99, 79
img = cv2.imread('C:\Users\peter\Documents\TestImages\pic99.jpg') #pulls image
imageNumber = 99

imgB = cv2.medianBlur(img,5) #works okay btw res2 is the one that goes down
imgB = cv2.morphologyEx(imgB,cv2.MORPH_OPEN,kernel)

res2 = imgB


#This stuff works, don't modify anything other than maybe the Canny parameters.
#Canny-on-color works very well. Try other values for science. Will have to adjust for general use
res2 = cv2.Canny(res2,150,350,True)


#Dilates to enhance contours, otherwise the contour-finder doesn't find them
img2 = cv2.dilate(res2,kernel,iterations = 2)


#Creates contours
img4, contours, hierarchy = cv2.findContours(img2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
img4 = img2
#img4 = cv2.cvtColor(img4,cv2.COLOR_GRAY2BGR)
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
                        #This following constant should depend on elevation!
                        kon = 60                        
                        #this crops or your image. min max functions prevent out of bounds errors!
                        cropped = res2[max(0,ellipse[0][1]-kon):min(ellipse[0][1]+kon,5232),max(0,ellipse[0][0]-kon):min(ellipse[0][0]+kon,3488)]
                        oldCropped = img[max(0,ellipse[0][1]-kon):min(ellipse[0][1]+kon,5232),max(0,ellipse[0][0]-kon):min(ellipse[0][0]+kon,3488)]    
                        cropped2 = cv2.dilate(cropped,kernel,iterations = 2)
                        croppednew, tempconts, hierarchtemp = cv2.findContours(cropped2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                        cv2.imwrite('C:\Users\peter\Documents\TestImages\RegionsOfInterest\Croppednew'+str(counter)+'from'+ str(imageNumber)+'.jpg',croppednew)

                        #filters out trees basically. if there's a lot of contours in the area, says image is bad. perhaps worth experimenting with different image sizes
                        if (len(tempconts) < 12):
                            goodshapes = goodshapes + [cropped2]
                            cv2.imwrite('C:\Users\peter\Documents\TestImages\RegionsOfInterest\RegionOfInterest'+str(counter)+'from'+ str(imageNumber)+'.jpg',oldCropped)
                    #else:
                        #img4 = cv2.ellipse(img4,ellipse,(0,255,255),2)

print len(goodshapes)




