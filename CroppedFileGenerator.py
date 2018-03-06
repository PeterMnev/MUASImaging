#if this doesn't import reinstall python probably / install proper libraries
import numpy as np
import cv2
from matplotlib import pyplot as plt

#Kernel for dilation. Can fiddle with it but doesn't really seem to affect end result much
kernel = np.ones((4,4),np.uint8)

#If you are on windows and you properly set up your repository in Documents\MUASImaging all you need to change is peter to your name
initialImage = cv2.imread('C:\Users\peter\Documents\MUASImaging\TestCases\Test3.jpg') #pulls image
imageNumber = 3 # Modify for file output

initialImage = cv2.medianBlur(initialImage,5) # Blurs Image in Preparation for Proc
initialImage = cv2.morphologyEx(initialImage,cv2.MORPH_OPEN,kernel) # Morph_Open does what you want it to do

#Separates this object from initial because I need to reference the initial later. How to optimize?
cannyImage = initialImage

#This changes image into contours.
cannyImage = cv2.Canny(cannyImage,150,350,True)

#Dilates to thicken the contours.

#Creates the array of contours.
#Interesting fact: if you change placeholder >>> cannyImage you get a filled shape. Unclear how reliable this would be.
cannyImage, contours, hierarchy = cv2.findContours(cv2.dilate(cannyImage,kernel,iterations = 2), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#Counter sort of deprecated but useful for debugging - calculate how many contours you successfully logged
counter = 0
resultingContours = []
PrevX = -420
PrevY = -420
#Iterates through contour list and creates files with cropped images.
for num in range(0,len(contours)):

    #mandatory filter or else runtime error - short contours dont work with ellipse function
    if len(contours[num]) > 4:

        ellipse = cv2.fitEllipse(contours[num])
        X = ellipse[0][0]
        Y = ellipse[0][1]
        #size based filtering,eventually update to incorporate altitude pixel - inch ratio in order to prevent objects that are way too small from getting caught
        #New: Filter based on duplicity        
        if (ellipse[1][0]+ ellipse[1][1] > 80) and ((abs(X - PrevX) > 10) or (abs(Y - PrevY) > 10)):

            if ellipse[1][0]+ ellipse[1][1] < 300:

                #a good filter for very long and eccentric things. Reduce value in order to mandate even more circular objects
                if (abs(ellipse[1][0] - ellipse[1][1]))/(ellipse[1][0] + ellipse[1][1]) < .4:   

                    area = cv2.contourArea(contours[num])
                    hull = cv2.convexHull(contours[num])
                    hull_area = cv2.contourArea(hull)
                    solidity = float(area)/hull_area
                    #some really squiggly shapes won't be accepted, unfortunately not a catch em all type filter
                    if solidity > .7:

                        counter = counter + 1
                        #This following constant should depend on elevation!
                        elevationConstant = 60                        
                        #this crops your image. min max functions prevent out of bounds errors!
                        cropped = cannyImage[max(0,ellipse[0][1]-elevationConstant):min(ellipse[0][1]+elevationConstant,5232),max(0,ellipse[0][0]-elevationConstant):min(ellipse[0][0]+elevationConstant,3488)]
                        oldCropped = initialImage[max(0,ellipse[0][1]-elevationConstant):min(ellipse[0][1]+elevationConstant,5232),max(0,ellipse[0][0]-elevationConstant):min(ellipse[0][0]+elevationConstant,3488)]    
                        cropped, tempconts, hierarchtemp = cv2.findContours(cropped, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                        #filters out trees basically. if there's a lot of contours in the area, says image is bad. perhaps worth experimenting with different image sizes
                        if ((len(tempconts) < 12)):

                            PrevX = X
                            PrevY = Y
                            resultingContours = resultingContours + [cropped]
                            cv2.imwrite('C:\Users\peter\Documents\MUASImaging\Output\OldCropped '+str(counter)+'from'+ str(imageNumber)+'.jpg',oldCropped)
                            cv2.imwrite('C:\Users\peter\Documents\MUASImaging\Output\Cropped '+str(counter)+'from'+ str(imageNumber)+'.jpg',cropped)






