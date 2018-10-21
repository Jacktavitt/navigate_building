#!/usr/bin/env python3
import CustomImage
import HandyTools as HT
import numpy as np
import cv2
import imutils
import os
import pytesseract

def drawSingleContour(image, c, *, color = (0,125,255)):
    '''e-z handle for cv2 implementation of calulating and drawing shape contours'''
    shape, approx= detectShape(c)
    _x, _y, _w, _h = cv2.boundingRect(c)
    weird_shape = catchWeirdShape(_w, _h)
    M=cv2.moments(c)
    area = float(M['m00'])
    if area > 50 and not weird_shape:
        cv2.drawContours(image, [approx], -1, color, 4)
        cv2.putText(image, (f'area: {area}'), (_x, _y), cv2.FONT_HERSHEY_SIMPLEX, .75, color, 2)
    return area

def catchWeirdShape(width, height):
    '''returns true of width to height ratio is between 1/2 and 2'''
    try:
        if HT.betwixt(0.5, width/height, 2):
            return False
    except ZeroDivisionError as e:
        return True


def actualVsLocalArea(contour_area, minrec_area):
    '''compare area of contour with area of min bounding rectangle
    to see if shape is near a rectangle'''
    diff = abs(contour_area - minrec_area)
    if contour_area is 0:
        return False
    ratio = diff/contour_area
    # areas under 50 are noise and will be weeded out here
    if ratio > 0.1 or contour_area < 50 or minrec_area < 50:
        return False

    return ratio

def drawSingleMinRec(image, c, *, doop=None):
    '''draw a min bounding rectangle and return area'''
    minrec = cv2.minAreaRect(c)
    box1 = cv2.boxPoints(minrec)
    bl, tl, tr, br = box1
    height = abs(bl[1]-tl[1])
    width = abs(tl[0]-tr[0])
    weird_shape = catchWeirdShape(width, height)
    bottom = (bl[0], bl[1])
    # area = cv2.contourArea(c)
    min_area = round((width * height), 2)
    box = np.int0(box1)
    mid = 0
    if min_area > 50 and not weird_shape:
        if doop:
            for count, item in enumerate(box):
                print(f'#{count}: {item}\n')
                cv2.circle(image, (item[0], item[1]), 10, (mid, 255-mid, 255), 3)
                mid += 55
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        cv2.drawContours(image, [box], 0, (100, 0, 255), 2)
        cv2.putText(image, (f'area: {min_area}'), (bl[0], bl[1]), cv2.FONT_HERSHEY_SIMPLEX,
                    .75, (125, 125, 255), 2)
    return min_area

def drawContours(image, contours):
    for c in contours:
        drawSingleContour(image, c)

def drawBoundingBoxes(image, contours):
    areas = []
    for c in contours:
        areas.append(drawSingleMinRec(image, c))
    return areas

def calibratePlaque(sourceImage):
    '''sets the area and shape to expect from room marking plaques
        what we need to find is a good size to judge the pother plaques by.
    '''
    # check what we're getting
    if isinstance(sourceImage, CustomImage.Image):
        image = sourceImage
    else:
        image = CustomImage.Image(sourceImage)
    # remove color from image
    gray = CustomImage.Image(image, copy=True)
    gray.gray()
    # initial open to reduce noise
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15)) 
    _thr, result = cv2.threshold(gray.image, 50, 255, cv2.THRESH_BINARY)
    opened = cv2.morphologyEx(result, cv2.MORPH_OPEN, kernel)
    # add canny edge detection
    edge_open = cv2.Canny(opened, 10, 255)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    closed = cv2.morphologyEx(edge_open, cv2.MORPH_CLOSE, kernel)
    # finf contours
    _, contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # draw contours and minimum bounding rectangles for each contour
    # get the areas back
    areas = {}
    for idx, contour in enumerate(contours):
        # print(f'idx: {idx}, lencont: {len(contour)}\n')
        areas[idx] = {}
        areas[idx]['contour'] = contour
        areas[idx]['contour_area'] = drawSingleContour(image.image, contour)
        areas[idx]['minred_area'] = drawSingleMinRec(image.image, contour)
        areas[idx]['ratio'] = actualVsLocalArea(areas[idx]['contour_area'],
                    areas[idx]['minred_area'])

    for key, value in enumerate(areas):
        if not areas[key]['ratio']:
            areas[key] = None
        if areas[key]:
            drawSingleContour(image.image, areas[key]['contour'], color=(255, 0, 100))
        # if areas[key]['ratio'] > 0.1:
        #     areas[key] = None
    print(areas)
    image.show()
    return areas

def detectShape(contour):
    '''returns what kind of shape has been found based on number of sides'''
    shape = ""
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.04*peri, True)
    if len(approx) == 3:
        shape = "Triangle"
    elif len(approx) == 4:
        shape = "Quadrilateral"
    elif len(approx) == 5:
        shape = "Pentagon"
    elif len(approx) < 10:
        shape = "Polygon"
    else:
        shape = "Circle"
    return shape, approx

def getContours(sourceImage):
    if isinstance(sourceImage, CustomImage.Image):
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

def markPlaque(sourceImage, good_ratio, good_area, *, do_crop=False, _debug=None, _save=None):
    '''
    sourceImage: CustomImage object
    good_ratio: best ratio for a plaque
    good_area: approximation of a good size for a plaque
    '''

    if isinstance(sourceImage, CustomImage.Image):
        image = sourceImage
    else:
        image = CustomImage.Image(sourceImage)

    gray = CustomImage.Image(image, copy=True)
    gray.gray()
    gray.blur()
    gray.thresh()
    contours = getContours(gray)
    for c in contours:
        shape, approx = detectShape(c)
        if shape is "Quadrilateral":
            contour_area = drawSingleContour(image.image, c)
            minred_area = drawSingleMinRec(image.image, c)
            ratio = actualVsLocalArea(contour_area, minred_area)
            # if do_crop:
            #     # crop out special part
            #     crop = CustomImage.Image(cmage.image[_y:_y+_h,_x:_x+_w, :])
            #     text = readPlaque(crop)
            #     cv2.putText(cmage.image, text,(_x+_w,_y+_h),cv2.FONT_HERSHEY_SIMPLEX,.5,linecolor,2)
            #     cmage.show()
            if contour_area > good_area - 200 and contour_area < good_area + 200:
                if ratio > good_ratio - 0.2 and ratio < good_ratio + 0.2:
                    drawSingleContour(image.image, c, color=(255, 75, 75))
    return image.image

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