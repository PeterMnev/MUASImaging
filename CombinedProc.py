import cv2
from matplotlib import pyplot as plt
plt.switch_backend('agg')
import os
import imutils
import numpy as np

print (os.path.dirname(os.path.abspath(__file__)))
#Kernel for dilation. Can fiddle with it but doesn't really seem to affect end result much
kernel = np.ones((5,5),np.uint8)

#If you are on windows and you properly set up your repository in Documents\MUASImaging all you need to change is peter to your name
initialImage = cv2.imread('/home/peter/Imaging/TestCases/Test1.jpg') #pulls image
imageNumber = 5 # Modify for file output
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

cv2.imwrite('/home/peter/Imaging/Intermediates/Contours.jpg', cv2.drawContours(cannyImage, contours, -1, (0,255,0), 3))

resultingContours = []
resulCont = []
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
                        cropped = cannyImage[max(0,int(ellipse[0][1])-elevationConstant):min(int(ellipse[0][1])+elevationConstant,5232),max(0,int(ellipse[0][0])-elevationConstant):min(int(ellipse[0][0])+elevationConstant,3488)]
                        oldCropped = initialImage[max(0,int(ellipse[0][1])-elevationConstant):min(int(ellipse[0][1])+elevationConstant,5232),max(0,int(ellipse[0][0])-elevationConstant):min(int(ellipse[0][0])+elevationConstant,3488)]    
                        cropped, tempconts, hierarchtemp = cv2.findContours(cropped, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                        #filters out trees basically. if there's a lot of contours in the area, says image is bad. perhaps worth experimenting with different image sizes
                        if ((len(tempconts) < 12)):
                            print("foundd")               
                            PrevX = X
                            PrevY = Y
                            print (oldCropped.size)
                            cv2.imwrite('/home/peter/Imaging/Output/OldyCropped'+str(counter)+'from'+ str(imageNumber)+'.jpg',oldCropped)
                            cv2.imwrite('/home/peter/Imaging/Output/Croppedy'+str(counter)+'from'+ str(imageNumber)+'.jpg',cropped)






#This is the initial image pull
initialImage = cv2.imread('/home/peter/Imaging/Output/OldyCropped2from5.jpg') #pulls imageZ = initialImage.reshape((-1,3))

##############PART ONE################
###########SHAPE RECOGNITION##########

#Begin K-Cluster - 2 Color
#Reshape > prepare for K-Cluster
Z = initialImage.reshape((-1,3))
Z = np.float32(Z)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10,1.0)
#One may say this is risky, but the predominant shapes are the main shape and the background. As long as shape is sufficient size to be the second peak of the histogram this is fine. May require adjusting!
K = 2
ret, label, center = cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
center = np.uint8(center)
res = center [label.flatten()]
dualColor = res.reshape((initialImage.shape))
cv2.imwrite('/home/peter/Imaging/Intermediates/AwesomeDual.jpg',dualColor)

#Begin color formatting
#Gets the color of the pixel in the top-left corner
a = (dualColor.item(10,10,2))

#Changes everything other than center shape to white, which in turn is now blackened
i = 0
j = 0
for row in dualColor:
    for row2 in row:
        if row2[2] == a:
            dualColor[i][j] = [200,200,200]
        else:
            dualColor[i][j] = [0,0,0]
        j += 1
    i += 1
    j = 0

#Now Erode. Erode works by making darker sections smaller.
kernel = np.ones((3,3),np.uint8)
dualColor = cv2.erode(dualColor, kernel, iterations = 1)

#Stores the mask for future use.
cv2.imwrite('/home/peter/Imaging/Intermediates/Mask.jpg',dualColor)
#Get shape
#Ideally you would loop through them
compareTo = cv2.imread('/home/peter/Imaging/Shapes/circle.png')
#################TODO: MAKE A FILE WITH CONTOURS PREPARED AS ARRAYS#############
dualColor = cv2.cvtColor(dualColor,cv2.COLOR_BGR2GRAY)
compareTo = cv2.cvtColor(compareTo,cv2.COLOR_BGR2GRAY)

#Thresholds the shape because it was incorrectly made white -.-
ret,compareTo = cv2.threshold(compareTo,127,255,cv2.THRESH_BINARY_INV)

#Contours Are Made - ideally only one would be made
ignorethis, contours, hierarchy = cv2.findContours(dualColor, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
print (len(contours))
cnt1 = contours[1]
ignorethis, contours, hierarchy = cv2.findContours(compareTo, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnt2 = contours[1]
print len(contours)
#Contour Comparison Function:
Value = cv2.matchShapes(cnt1,cnt2,1,0.0)
print ("how matchy shape")
print (Value)



################PART TWO################
##########CHARACTER CLEANUP #############
initialImage = cv2.imread('/home/peter/Imaging/Output/OldyCropped2from5.jpg')
mask = cv2.imread('/home/peter/Imaging/Intermediates/Mask.jpg')    

kernel = np.ones((5,5),np.uint8)
mask = cv2.dilate(mask,kernel,iterations = 1)
mask = cv2.cvtColor(mask,cv2.COLOR_BGR2GRAY) #Converts to grayscale
ret,mask = cv2.threshold(mask,127,255,cv2.THRESH_BINARY_INV) #Invert
masked = cv2.bitwise_and(initialImage,initialImage,mask = mask)


#Begin Tri-Color KCluster
Z = masked.reshape((-1,3))
Z = np.float32(Z)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10,1.0)
#3 Colors
K = 3
ret, label, center = cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
center = np.uint8(center)
res = center [label.flatten()]
triColor = res.reshape((masked.shape))
cv2.imwrite('/home/peter/Imaging/Intermediates/ColoredTripleColor.jpg',triColor)
#Creates a histogram
forHistogram = cv2.cvtColor(triColor, cv2.COLOR_BGR2GRAY)
histo = plt.hist(forHistogram.ravel(),256,[0,256])

#Identifies Least Common Color (in greys)
maxi = 10000
indexi = 0
for i in range(0,len(histo[0])):
    b = histo[0][i]
    if b != 0:
        if b <= maxi:
            indexi = i
            maxi = b

triColor = cv2.cvtColor(triColor,cv2.COLOR_BGR2GRAY)
cv2.imwrite('/home/peter/Imaging/Intermediates/Awesome.jpg',triColor)
#Makes Everything but center letter white, which in turn turns black.
i=0
j=0
for row in triColor:
    for row2 in row: 
        if row2 != indexi :
            triColor[i][j] = 200
        else:
            triColor[i][j]=0
        j += 1
    i += 1
    j = 0


kernel = np.ones((2,2),np.uint8)



triColor = cv2.dilate(triColor,kernel,iterations = 1)

#triColor = imutils.rotate_bound(triColor, 270)
#riColor = imutils.resize(triColor, 500)
#triColor = cv2.GaussianBlur(triColor,(9,9),0)
cv2.imwrite('/home/peter/Imaging/Intermediates/OnlyLetters.jpg',triColor)



for letter in ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']:
    
    Base = cv2.imread('/home/peter/Imaging/Letters/Letter'+str(letter)+'.png')

    Base = cv2.cvtColor(Base,cv2.COLOR_BGR2GRAY)

    ret,Base = cv2.threshold(Base,127,255,cv2.THRESH_BINARY_INV) #Invert
    
    cv2.imwrite('/home/peter/Imaging/Intermediates/WhatICompareTo.jpg',Base)
    ignorethis, contours, hierarchy = cv2.findContours(triColor, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print ("number of contours rom triColor dual color image")
    print (len(contours))
    cnt1 = contours[1]
    ignorethis, contours, hierarchy = cv2.findContours(Base, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print ("number of contours rom base image")
    print (len(contours))
    cnt2 = contours[1]
    ret = cv2.matchShapes(cnt1,cnt2,1,0.0)
    print ("How much does it match"+letter)
    print (ret)








