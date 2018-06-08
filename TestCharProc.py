import numpy as np
import cv2
from matplotlib import pyplot as plt
import os

triColor = cv2.imread('C:\Users\peter\Documents\MUASImaging\Intermediates\OnlyLetters.jpg')
Base = cv2.imread('C:\Users\peter\Documents\MUASImaging\Letters\LetterU.png')
triColor = cv2.cvtColor(triColor,cv2.COLOR_BGR2GRAY)

(thresh, triColor) = cv2.threshold(triColor, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

Base = cv2.cvtColor(Base,cv2.COLOR_BGR2GRAY)
ret,Base = cv2.threshold(Base,127,255,cv2.THRESH_BINARY_INV) #Invert
ignorethis, contours, hierarchy = cv2.findContours(triColor, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
print "len contours triColor"
print len(contours)
cnt1 = contours[1]
ignorethis, contours, hierarchy = cv2.findContours(Base, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
print "len contours base"
print contours
cnt2 = contours[1]
ret = cv2.matchShapes(cnt1,cnt2,1,0.0)
print ret
