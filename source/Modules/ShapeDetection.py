#!/usr/bin/env python3
import CustomImage
import numpy as np
import cv2
import imutils
import os
import pytesseract
from decimal import *
getcontext().prec = 2

def drawSingleContour(image, c):
    shape, approx= detectShape(c)
    _x, _y, _w, _h = cv2.boundingRect(c)
    M=cv2.moments(c)
    area = float(M['m00'])
    if area > 50:
        cv2.drawContours(image, [approx], -1, (125, 255, 0), 4)
        # cv2.putText(image, str(area)+' '+str(shape),(_x,_y),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,125,255),2) 

def drawSingleMinRec(image, c, *, doop=None):
    '''draw a min bounding rectangle and return area'''
    minrec = cv2.minAreaRect(c)
    box1 = cv2.boxPoints(minrec)
    bl, tl, tr, br = box1

    height = abs(bl[1]-tl[1])
    width = abs(tl[0]-tr[0])
    bottom = (bl[0], bl[1])
    area = cv2.contourArea(c)
    min_area = width * height
    box = np.int0(box1)
    M = cv2.moments(c)
    area = float(M['m00'])
    mid = 0
    area_diff = None
    if area > 50:
        if doop:
            for count, item in enumerate(box):
                print(f'#{count}: {item}\n')
                cv2.circle(image, (item[0], item[1]), 10, (mid, 255-mid, 255), 3)
                mid += 55
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        cv2.drawContours(image, [box], 0, (100, 0, 255), 2)
        cv2.putText(image, (f'area: {area}'), (tl[0], tl[1]), cv2.FONT_HERSHEY_SIMPLEX,
                    .5, (0, 125, 255), 2)
        cv2.putText(image, (f'min_area: {min_area}'), bottom, cv2.FONT_HERSHEY_SIMPLEX,
                    .5, (255, 125, 0), 2)
        area_diff = abs(area - min_area)
    return area_diff

def drawContours(image, contours):
    for c in contours:
        drawSingleContour(image, c)

def drawBoundingBoxes(image, contours):
    areas = []
    for c in contours:
        areas.append(drawSingleMinRec(image, c))
    return areas


def calibratePlaque(sourceImage):
    '''sets the area and shape to expect from room marking plaques''' 
    if type(sourceImage) == CustomImage.Image:
        image = sourceImage
    else:
        image = CustomImage.Image(sourceImage)
    gray = CustomImage.Image(image, copy=True)
    gray.gray()
    # initial open to reduce noise
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15)) 
    _thr, result = cv2.threshold(gray.image, 50, 255, cv2.THRESH_BINARY)
    opened = cv2.morphologyEx(result, cv2.MORPH_OPEN, kernel)

    edge_open = cv2.Canny(opened, 10, 255)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    closed = cv2.morphologyEx(edge_open, cv2.MORPH_CLOSE, kernel)

    im2, contours, x = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    drawContours(image.image, contours)
    diffed_areas = drawBoundingBoxes(image.image, contours)
    print(diffed_areas)
    image.show()


def actualVsLocalArea(c):
    _x,_y,_w,_h = cv2.boundingRect(c)
    minrec = cv2.minAreaRect(c)
    box=cv2.boxPoints(minrec)
    box=np.int0(box)
    print(box)
    M=cv2.moments(c) 
    localArea = float(M['m00'])
    boundingarea = _w*_h


def detectShape(contour):
    '''returns what kind of shape has bee found based on number of sides'''
    shape = ""
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.04*peri, True)
    if len(approx)==3:
        shape = "Triangle"
    elif len(approx)==4:
        shape = "Quadrilateral"
    elif len(approx)==5:
        shape = "Pentagon"
    else:
        shape = "Circle"
    return shape, approx

def getContours(sourceImage):
    if type(sourceImage) == CustomImage.Image:
        image = sourceImage
    else:
        image = CustomImage.Image(sourceImage)
    # its edgin' time
    edged = cv2.Canny(image.image,10,250)
    #fill gaps
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    # closed = CIMAGE(cv2.morphologyEx(edged.image, cv2.MORPH_CLOSE, kernel))
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
    im2,contours,x= cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def markPlaque(sourceImage, *, showstuff=None, _debug=None, _save=None):
    '''
    image: CustomImage object
    showstuff: if true, shows the cropped image
    '''
    if type(sourceImage) == CustomImage.Image:
        cmage = sourceImage
    else:
        cmage = CustomImage.Image(sourceImage)
    cmage.resize(vertical=512)
    image = CustomImage.Image(cmage, copy=True)
    image.gray()
    image.blur()
    image.thresh()
    contours = getContours(image)

    for c in contours:
        linecolor = (0,255,0)
        textcolor = (0,125,255)
        if _debug:
            # image.addColor()
            cmage = image
            linecolor = (125)
            textcolor = (125)
        shape,approx = detectShape(c)
        if shape is "Quadrilateral":
            # get location
            _x,_y,_w,_h = cv2.boundingRect(c)
            if showstuff:
                # crop out special part
                crop = CustomImage.Image(cmage.image[_y:_y+_h,_x:_x+_w, :])
                text = readPlaque(crop)
                cv2.putText(cmage.image, text,(_x+_w,_y+_h),cv2.FONT_HERSHEY_SIMPLEX,.5,linecolor,2)
                cmage.show()
            
            M=cv2.moments(c)
            area = float(M['m00'])
            if area > 2500 and area < 5000:
                cv2.drawContours(cmage.image,[approx], -1, linecolor, 4)
                cv2.putText(cmage.image, str(area),(_x,_y),cv2.FONT_HERSHEY_SIMPLEX,.5,textcolor,2)
                if _save:
                    crop = CustomImage.Image(cmage.image[_y:_y+_h,_x:_x+_w, :])
                    crop.save(imagePath=f'/home/johnny/tempthesis/{_save}_{area}.png')
            # print("Area: {}".format(M['m00']))
            
            # total +=1
    return cmage.image

def readPlaque(crop):
    '''
    takes CustomImage and tries to read the text inside.
    '''
    crop.gray()
    # crop.blur()
    crop.show()
    # crop.image = cv2.adaptiveThreshold(crop.image,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)
    # ret,crop.image=cv2.threshold(crop.image,127,255,cv2.THRESH_BINARY)
    # crop.show()
    text = pytesseract.image_to_string(crop.image)
    print('text: '+text)
    things = pytesseract.image_to_boxes(crop.image)
    print('things: '+things) 


    return text