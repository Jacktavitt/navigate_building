#!/usr/bin/env python3
import CustomImage
import HandyTools as HT
import numpy as np
from PIL import Image, ImageTk
import cv2
import imutils
import os
import pytesseract
import tkinter as tk
import string
ALL_CHARS = string.ascii_letters + string.digits


def drawSingleContour(image, c, *, text=None, color=(0, 125, 255), to_draw=True):
    '''e-z handle for cv2 implementation of calulating and drawing shape contours'''
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.04*peri, True)
    _x, _y, _w, _h = cv2.boundingRect(c)

    M = cv2.moments(c)
    area = float(M['m00'])
    text = area if not text else text
    if area > 50 and to_draw:
        cv2.drawContours(image, [approx], -1, color, 4)
        cv2.putText(image, (f'{text}'), (_x+int(_w/2), _y+int(_h/2)), cv2.FONT_HERSHEY_SIMPLEX, .75, color, 2)
    return area, (_w, _h), (_x, _y)

def catchWeirdShape(width, height):
    '''TOFDO write this'''
    try:
        # if HT.betwixt(0.5, width/height, 2):
        return not HT.betwixt(0.5, width/height, 2)
    except ZeroDivisionError as e:
        return True

def actualVsMBRArea(contour_area, minrec_area):
    '''return ratio of area of minimum bounding rectangle to contour's area
        idea is that min bounding rec should be close to contour area if it is a rectangle
    '''
    if contour_area is 0:
        return 0
    ratio = minrec_area/contour_area
    return abs(ratio)

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
    return min_area, (width, height), (bl, tl, tr, br)

def drawContours(image, contours):
    for c in contours:
        drawSingleContour(image, c)

def drawBoundingBoxes(image, contours):
    areas = []
    for c in contours:
        areas.append(drawSingleMinRec(image, c))
    return areas

def calibratePlaque(source_image):
    '''sets the area and shape to expect from room marking plaques
        what we need to find is a good size to judge the pother plaques by.
    '''
    # check what we're getting
    if isinstance(source_image, CustomImage.Image):
        image = source_image
    else:
        image = CustomImage.Image(source_image)
    # remove color from image
    gray = CustomImage.Image(image, copy=True)
    gray.gray()
    gray.thresh(thresh_num=50)
    contours = canny_edge_and_contours(gray)
    # lets show an image of the contours, they each have a name
    # and a radio button to choose the right one
    areas = {}
    chosen_value = None

    window = tk.Tk()
    window.title("Please Choose Correct Contour")
    window.configure(background='grey')

    PIXEL = tk.PhotoImage(width=1, height=1)

    listbox = tk.Listbox(window)
    listbox.pack(side='right')
    # scrollbar = tk.Scrollbar(listbox)
    # scrollbar.pack(side='right', fill='y')
    chosen = tk.StringVar()
    chosen.trace('w', simpleCallBack)

    def showChoice():
        print(chosen.get())

    def CloseWindow():
        print(f"close window!")
        if chosen.get():
        # if chosen_value:
            window.destroy()

    numbad = 0
    numgood = 0
    for idx, contour in enumerate(contours):
        # print(f'idx: {idx}, lencont: {len(contour)}\n')
        try:
            label = ALL_CHARS[numgood]
        except Exception as e:
            print(e)
            label = 'TILT'

        areas[idx] = {}
        areas[idx]['label'] = label
        areas[idx]['contour'] = contour
        areas[idx]['contour_area'], (areas[idx]['contour_w'], areas[idx]['contour_h']), (x, y) = drawSingleContour(image.image, contour)
        areas[idx]['minred_area'], mrwh, bl_tl_tr_br = drawSingleMinRec(image.image, contour)
        areas[idx]['ratio'] = actualVsMBRArea(areas[idx]['contour_area'],
                    areas[idx]['minred_area'])

        if catchWeirdShape(areas[idx]['contour_w'],
                           areas[idx]['contour_h']) or catchWeirdShape(mrwh[0], mrwh[1]):
            areas[idx]['valid'] = False
            numbad += 1
        else:
            areas[idx]['valid'] = True
            drawSingleContour(image.image, areas[idx]['contour'], color=(255, 0, 100), text=str(label))
            if numgood%10 == 0:
                radioholder = tk.Listbox(listbox)
                radioholder.pack(side='left')
            tk.Radiobutton(radioholder, text=label, padx=20, variable=chosen, command=showChoice, value=str(idx)).pack(side='top')
            numgood += 1

    img = Image.fromarray(image.image)
    img = ImageTk.PhotoImage(img)
    panel = tk.Label(window, image=img)
    panel.pack(side='bottom', fill='both', expand='yes')
    window.update()
    tk.Button(window, text="CONFIRM SELECTION", image=PIXEL, command=CloseWindow, compound='c', width=(image.get_width())).pack(side='top')
    window.mainloop()

    print(f"chosen item: {chosen.get()} in the result:{areas[int(chosen.get())]}")
    # print(f"just for shits: whole area dictionary: {areas}")
    return areas[int(chosen.get())]

def simpleCallBack(*args):
    print(f'variable changed {args}')

def calibration_interface(areas_dictionary):
    '''show image and radio buttons for each contour, user picks the right one'''
    pass

def detectShape(approx):
    '''returns what kind of shape has been found based on number of sides'''
    shape = ""
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
    return shape

def canny_edge_and_contours(source_image, *, threshold_1=50, threshold_2=250):
    if isinstance(source_image, CustomImage.Image):
        image = source_image
    else:
        image = CustomImage.Image(source_image)
    # its edgin' time
    edged = cv2.Canny(image.image, threshold_1, threshold_2)
    #fill gaps
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    # closed = CIMAGE(cv2.morphologyEx(edged.image, cv2.MORPH_CLOSE, kernel))
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
    _, contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def markPlaque(source_image, *, good_ht, good_wd, do_crop=False, _debug_mode=False, _save=None):
    '''
    source_image: CustomImage object
    good_ratio: best ratio for a plaque
    good_area: approximation of a good size for a plaque
    '''
    # set up boundaries for height and width
    # print(f'{_debug_mode}\n')
    min_ht = 0.85*good_ht
    max_ht = 1.15*good_ht
    min_wid = 0.85*good_wd
    max_wid = 1.15*good_wd

    if isinstance(source_image, CustomImage.Image):
        image = source_image
    else:
        image = CustomImage.Image(source_image)
    clean_copy = CustomImage.Image(image)
    gray = CustomImage.Image(image)
    gray.gray()
    
    # gray.blur()
    # gray.image = cv2.Laplacian(gray.image, cv2.CV_64F)
    # gray.image = cv2.Sobel(gray.image, cv2.CV_64F, 1, 0, ksize=5)
    # gray.image = cv2.Sobel(gray.image, cv2.CV_64F, 0, 1, ksize=1)
    # gray.image = gray.image.astype(np.uint8)
    # gray.blur()
    ################################################# DANGER ZONE
    # ZONA PELIGROSA ############################################
    # to run through more thresholds ############################
    thr_vals = [150, 175, 200, 225, 250]
    for val in thr_vals:
        gary = CustomImage.Image(gray)
        gary.thresh(thresh_num=val)
        if _debug_mode:
            image = CustomImage.Image(gary)
            image.addColor()
        contours = canny_edge_and_contours(gary) #, threshold_1=10, threshold_2=200)
        counter = 0
        for c in contours:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.04*peri, True)
            # shape = detectShape(approx)
            # if shape is "Quadrilateral":
            if len(approx) == 4:
                contour_area, (c_width, c_height), (_x, _y) = drawSingleContour(image.image, c, to_draw=_debug_mode)
                # minred_area, mrhw, bounds = drawSingleMinRec(image.image, c)

                if HT.betwixt(min_wid, c_width, max_wid) and HT.betwixt(min_ht, c_height, max_ht):
                    # print("this one is good\n")
                    _, (_w, _h), (_x, _y) = drawSingleContour(image.image, c, color=(255, val, val-90))
                    if do_crop:
                        crop = CustomImage.Image(clean_copy.image[_y:_y+_h, _x:_x+_w, :])
                        file_path = f"{_save}{counter}.png"
                        crop.save(file_path=file_path)
                        counter += 1

    return image.image

def readPlaque(crop):
    '''
    takes CustomImage and tries to read the text inside.
    '''
    gray = CustomImage.Image(crop)
    gray.gray()
    # gray.blur()
    gray.thresh(thresh_num=200)
    # kernel = np.ones((25, 25), np.uint8)
    gray.blur(kernel=(3, 3))
    # gray.show()
    # closed = cv2.morphologyEx(gray.image, cv2.MORPH_CLOSE, kernel)
    # opened = cv2.morphologyEx(gray.image, cv2.MORPH_OPEN, kernel)
    # HT.showKill(opened)

    # crop.blur()
    # crop.show()
    # crop.image = cv2.adaptiveThreshold(crop.image,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)
    # ret,crop.image=cv2.threshold(crop.image,127,255,cv2.THRESH_BINARY)
    # crop.show()
    text = pytesseract.image_to_string(gray.image)
    # if text:
    #     print(f'text: {text}\nfile: {crop.file_path}')
    # crop.addColor()
    cv2.putText(crop.image, text, (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (250, 0, 125), 2)
    # things = pytesseract.image_to_boxes(gray.image)
    # print('things: '+things)

    return text, crop