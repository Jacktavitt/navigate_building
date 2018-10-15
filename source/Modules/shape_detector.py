#!/usr/bin/env python3
import CustomImage as CIM
import numpy as np
import cv2
import imutils
import os
import pytesseract

def detectShape(contour):
    '''returns what kind of shape has bee found based on number of sides'''
    shape=""
    peri = cv2.arcLength(contour,True)
    approx = cv2.approxPolyDP(contour, 0.04*peri, True)
    if len(approx)==3:
        shape="Triangle"
    elif len(approx)==4:
        shape = "Quadrilateral"
    elif len(approx)==5:
        shape = "Pentagon"
    else:
        shape = "Circle"
    return shape,approx



'''
Finds a probable wall plaque given pixel size restrictions.
outlines the plaque.
'''

def markPlaque(sourceImage):
    '''
    image: CustomImage object
    '''
    # CIMAGE = CIM.Image
    # cmage = CIMAGE(sourceImage)
    cmage = sourceImage
    cmage.resize(vertical=512)
    image = CIM.Image(cmage, copy=True)
    image.gray()
    image.blur()
    # its edgin' time
    # edged = CIMAGE(cv2.Canny(image.image,10,250))
    edged = cv2.Canny(image.image,10,250)
    #fill gaps
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    # closed = CIMAGE(cv2.morphologyEx(edged.image, cv2.MORPH_CLOSE, kernel))
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
    im2,contours,x= cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    total = 0

    for c in contours:
        shape,approx = detectShape(c)
        if shape is "Quadrilateral":
            # get location
            _x,_y,_w,_h = cv2.boundingRect(c)
            # crop out special part
            crop = CIM.Image(cmage.image[_y:_y+_h,_x:_x+_w, :])
            text = readPlaque(crop)

            cv2.drawContours(cmage.image,[approx], -1, (0,255,0), 4)
            M=cv2.moments(c)
            
            # must create new image to look for letters
            
            cv2.putText(cmage.image, str(M['m00']),(_x,_y),cv2.FONT_HERSHEY_SIMPLEX,.5,(255,0,125),2)
            cv2.putText(cmage.image, text,(_x+_w,_y+_h),cv2.FONT_HERSHEY_SIMPLEX,.5,(255,125,125),2)
            # print("Area: {}".format(M['m00']))
            cmage.show()
            total +=1

def readPlaque(crop):
    '''
    takes CustomImage and tries to read the text inside.
    '''
    crop.gray()
            
    crop.show()
    text = pytesseract.image_to_string(crop.image)
    print('text: '+text)


    return text