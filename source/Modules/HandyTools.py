#!/usr/bin/env python3

import os
import cv2

def getFilesInDirectory(directory, fileType):
    fileList=[]
    for item in os.listdir(directory):
        if item.lower().endswith(fileType):
            fileList.append("{}{}".format(directory, item))
    return fileList

def hiLow255(num):
    return 0 if num > 122 else 255

def showKill(image, *, title=None):
    '''takes cv2 image and shows it.
        if something goes wrong and window is clicked closed, it will recover.
    '''
    title = title if title else "image"
    status = 1
    try:
        cv2.imshow(title, image)
        while status > 0:
            ks=cv2.waitKey(1000)
            try:
                status = cv2.getWindowProperty(title,cv2.WND_PROP_VISIBLE)
            except Exception as e:
                status = -1
                break
            if ks > 0:
                break
        cv2.destroyWindow(title)
    except Exception as e:
        print("error occured: {}",e)
        raise

def betwixt(less_num, target, great_num):
    '''true if target falss between less_num and great_num'''
    return(less_num < target and target < great_num)
