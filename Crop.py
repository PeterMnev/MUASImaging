import cv2
from matplotlib import pyplot as plt
plt.switch_backend('agg')
import os
import imutils
import numpy as np
import time
import sys

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#
#you need to change this depending on where you put the script itself, the folders where the images are being put into, and which folder you can output to
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#
imIn = (os.path.dirname(os.path.abspath(__file__)) + '/TestCases/')


#Change this to set where you will output cropped images, default is folder where script is run + output (create folder first!!!!)
imOut = (os.path.dirname(os.path.abspath(__file__)) + '/Output/')


#Kernel for dilation. Can fiddle with it but doesn't really seem to affect end result much
kernel = np.ones((5,5),np.uint8)
imageNumber = 1
pTime = time.time()
while True:
	cTime= time.time()

	#Change delay to match the timing of our pictures
	if (cTime - pTime > 1):
		print (imageNumber)
		pTime = cTime
		#If you are on windows and you properly set up your repository in Documents\MUASImaging all you need to change is peter to your name
		try:		
			initialImage = cv2.imread(imIn + 'Test' + str(imageNumber) + '.jpg') #pulls image
			initialImage = cv2.medianBlur(initialImage,5) # Blurs Image in Preparation for Proc
			initialImage = cv2.morphologyEx(initialImage,cv2.MORPH_OPEN,kernel) # Morph_Open does what you want it to do

			#Separates this object from initial because I need to reference the initial later. How to optimize?
			cannyImage = initialImage
			cannyImage = cv2.medianBlur(cannyImage,5)

			#This changes image into contours.
			cannyImage = cv2.Canny(cannyImage,150,350,True)

			#Dilates to thicken the contours.

			#Creates the array of contours.
			#Interesting fact: if you change placeholder >>> cannyImage you get a filled shape. Unclear how reliable this would be.
			cannyImage, contours, hierarchy = cv2.findContours(cv2.dilate(cannyImage,kernel,iterations = 2), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
			#Counter sort of deprecated but useful for debugging - calculate how many contours you successfully logged
			counter = 0

			#cv2.imwrite(imOut + 'Contours.jpg', cv2.drawContours(cannyImage, contours, -1, (0,255,0), 3))

			resultingContours = []
			resulCont = []
			PrevX = -1000
			PrevY = -1000
			#Iterates through contour list and creates files with cropped images.

			for num in range(0,len(contours)):

			    #mandatory filter or else runtime error - short contours dont work with ellipse function
			    if len(contours[num]) > 4:

				ellipse = cv2.fitEllipse(contours[num])
				X = ellipse[0][0]
				Y = ellipse[0][1]
				#size based filtering,eventually update to incorporate altitude pixel - inch ratio in order to prevent objects that are way too small from getting caught
				#New: Filter based on duplicity        
				if (ellipse[1][0]+ ellipse[1][1] > 100) and ((abs(X - PrevX) > 30) or (abs(Y - PrevY) > 30)):

				    if ellipse[1][0]+ ellipse[1][1] < 300:

					#a good filter for very long and eccentric things. Reduce value in order to mandate even more circular objects
					if (abs(ellipse[1][0] - ellipse[1][1]))/(ellipse[1][0] + ellipse[1][1]) < .3:   

					    area = cv2.contourArea(contours[num])
					    hull = cv2.convexHull(contours[num])
					    hull_area = cv2.contourArea(hull)
					    solidity = float(area)/hull_area
					    #some really squiggly shapes won't be accepted, unfortunately not a catch em all type filter
					    if solidity > .73:
						
						counter = counter + 1
						#This following constant should depend on elevation!
						elevationConstant = 60                        
						#this crops your image. min max functions prevent out of bounds errors!
						cropped = cannyImage[max(0,int(ellipse[0][1])-elevationConstant):min(int(ellipse[0][1])+elevationConstant,5232),max(0,int(ellipse[0][0])-elevationConstant):min(int(ellipse[0][0])+elevationConstant,3488)]
						oldCropped = initialImage[max(0,int(ellipse[0][1])-elevationConstant):min(int(ellipse[0][1])+elevationConstant,5232),max(0,int(ellipse[0][0])-elevationConstant):min(int(ellipse[0][0])+elevationConstant,3488)]    
						cropped, tempconts, hierarchtemp = cv2.findContours(cropped, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
						#filters out trees basically. if there's a lot of contours in the area, says image is bad. perhaps worth experimenting with different image sizes
						if ((len(tempconts) < 12)):
						    print("Region Of Interest Found")               
						    PrevX = X
						    PrevY = Y
						    print (oldCropped.size)
						    cv2.imwrite(imOut + 'OriginalCropped'+str(counter)+'from'+ str(imageNumber)+'.jpg',oldCropped)
						    cv2.imwrite(imOut + 'Cropped'+str(counter)+'from'+ str(imageNumber)+'.jpg',cropped)
		except:
			print ("Failed to find image with number " + str(imageNumber))
			print (sys.exc_info()[0])
		imageNumber = int(imageNumber) + 1
