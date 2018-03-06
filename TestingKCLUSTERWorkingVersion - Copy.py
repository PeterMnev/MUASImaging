import numpy as np
import cv2
from matplotlib import pyplot as plt

initialImage = cv2.imread('C:\Users\peter\Documents\TestImages\RegionsOfInterest\RegionOfInterest1from99_2.jpg') #pulls image 

Z = initialImage.reshape((-1,3))
Z = np.float32(Z)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10,1.0)
#One may say this is risky, but the predominant shapes are the main shape and the background. As long as shape is sufficient size to be the second peak of the histogram this is fine. May require adjusting!
K = 2
ret, label, center = cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
center = np.uint8(center)
res = center [label.flatten()]
res2 = res.reshape((initialImage.shape))

#This pixel is one from the corner of the image so it should not be part of the color shape
a = (res2.item(10,10,2))

i=0
j=0

#This is probably INCREDIBLY bad practice but this is being done for testing purposes! It works fine and fast though
for row in res2:
    for row2 in row:
        if row2[2] == a:
            res2[i][j] = [255,255,255]
        else:
            res2[i][j] = [0,0,0]
        j += 1
    i += 1
    j = 0

kernel = np.ones((5,5),np.uint8)
#erode makes the black space larger to constrict the shape
res2 = cv2.erode(res2,kernel,iterations = 1)
cv2.imwrite('C:\Users\peter\Documents\TestImages\RegionsOfInterest\BlackWhited.jpg',res2)
Base = cv2.imread('C:\Users\peter\Documents\TestImages\RegionsOfInterest\CrossShrunk.jpg') #pulls image 

#changes to black white color space on everythng
res2 = cv2.cvtColor(res2,cv2.COLOR_BGR2GRAY)
Base = cv2.cvtColor(Base,cv2.COLOR_BGR2GRAY)

#thresholding for proper coloration
ret,res2 = cv2.threshold(res2,127,255,cv2.THRESH_BINARY_INV)
ret,Base = cv2.threshold(Base,127,255,cv2.THRESH_BINARY_INV)
cv2.imwrite('C:\Users\peter\Documents\TestImages\RegionsOfInterest\BlackWhited.jpg',Base)
cv2.imwrite('C:\Users\peter\Documents\TestImages\RegionsOfInterest\BlackWhited2.jpg',res2)

#Gets the contours of both things. perhaps i should just save these for the existing one so that i dont have to do every single time. im dumb
ignorethis, contours, hierarchy = cv2.findContours(res2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

cnt1 = contours[0]
ignorethis, contours, hierarchy = cv2.findContours(Base, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

cnt2 = contours[0]

#magic function that matches the shapes. works best if shape is white outside is black
ret = cv2.matchShapes(cnt1,cnt2,1,0.0)
print "do the shapes match? lower is better"
print ret

#now for the character recognition
#start by loading original image and the black whited overlay.
img1 = cv2.imread('C:\Users\peter\Documents\TestImages\RegionsOfInterest\RegionOfInterest1from99_2.jpg')
img2 = cv2.imread('C:\Users\peter\Documents\TestImages\RegionsOfInterest\BlackWhited2.jpg')
kernel = np.ones((7,7),np.uint8)
img2 = cv2.erode(img2,kernel,iterations = 1)
img2 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY) #Converts to grayscale


                
img1_bg = cv2.bitwise_and(img1,img1,mask = img2)

cv2.imwrite('C:\Users\peter\Documents\MUASImaging\Output\Step3.jpg',img1_bg)

img1 = cv2.imread('C:\Users\peter\Documents\TestImages\RegionsOfInterest\RegionOfInterest1from99_2.jpg')

Z = img1_bg.reshape((-1,3))
Z = np.float32(Z)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10,1.0)
#3 Colors
K = 3
ret, label, center = cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
center = np.uint8(center)
res = center [label.flatten()]
res2 = res.reshape((img1.shape))

cv2.imwrite('C:\Users\peter\Documents\TestImages\RegionsOfInterest\TriColorKCluster.jpg',res2)
#in reality one would use a histogram to find the least common color of the 3 - black shape color and letter color. This would isolate the letter.

forHistogram = cv2.cvtColor(res2, cv2.COLOR_BGR2GRAY)

histo = plt.hist(forHistogram.ravel(),256,[0,256])
#TO-DO find a way to find the second largest value.
maxi = 10000
indexi = 0
for i in range(0,len(histo[0])):
    b = histo[0][i]
    if b != 0:
        if b <= maxi:
            indexi = i
            maxi = b
print indexi
res2 = cv2.cvtColor(res2,cv2.COLOR_BGR2GRAY)

i=0
j=0
for row in res2:
    for row2 in row: 
        if row2 != indexi :
            res2[i][j] = 0
        j += 1
    i += 1
    j = 0

ret,res2 = cv2.threshold(res2,10,255,cv2.THRESH_BINARY_INV)
ret,res2 = cv2.threshold(res2,10,255,cv2.THRESH_BINARY_INV)
kernel = np.ones((3,3),np.uint8)

res2 = cv2.erode(res2,kernel,iterations = 1)
res2 = cv2.dilate(res2,kernel,iterations = 2)




cv2.imwrite('C:\Users\peter\Documents\TestImages\RegionsOfInterest\AfterProcForLetter.jpg',res2)
Base = cv2.imread('C:\Users\peter\Documents\TestImages\RegionsOfInterest\LetterI.png')
Base = cv2.cvtColor(Base,cv2.COLOR_BGR2GRAY)
ignorethis, contours, hierarchy = cv2.findContours(res2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
print len(contours)
cnt1 = contours[0]
ignorethis, contours, hierarchy = cv2.findContours(Base, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
print len(contours)
cnt2 = contours[0]
ret = cv2.matchShapes(cnt1,cnt2,1,0.0)
print ret



print('done')
