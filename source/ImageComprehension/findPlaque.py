#!/usr/bin/env python3
import CustomImage as CIM
import cv2
import numpy as np

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
    image = CIMAGE(cmage, copy=True)
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
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02*peri, True)
        if len(approx) is 4:
            cv2.drawContours(cmage.image,[approx], -1, (0,255,0), 4)
            M=cv2.moments(c)
            _x,_y,_w,_h = cv2.boundingRect(c)
            cv2.putText(cmage.image, str(M['m00']),(_x,_y),cv2.FONT_HERSHEY_SIMPLEX,.5,(255,0,125),2)
            # print("Area: {}".format(M['m00']))
            cmage.show()
            total +=1
