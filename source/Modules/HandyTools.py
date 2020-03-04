#!/usr/bin/env python3

import os
import cv2
import argparse
import numpy

def getFilesInDirectory(directory, fileType):
    return [os.path.join(directory, item) for item in os.listdir(directory) if item.lower().endswith(fileType)]

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

def add_prefix_to_file(filepath, prefix):
    '''
    sets prefix in front of a filename and returns amended path
    sample filepath: 'train/plaques/002999.png'
    sample prefix: '0_'
    '''
    directory, file_name = os.path.split(filepath)
    file_name = prefix + file_name
    changed_path = os.path.join(directory, file_name)
    return changed_path

def str2bool(word):
    '''
    from 'Maxim's response to https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse
    will evaluate a string as a true or false
    '''
    if word.lower() in ('yes','true','y','t','yep','1','ok'):
        return True
    elif word.lower() in ('no','false','n','f','nope','0','nah','fuck you'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected. Very disappointed')

def distill_list(list_of_elements):
    '''
    takes a list of many items and removes all adjacent duplicates.
    '''
    new_list = []
    cur_idx = 0
    now_val = list_of_elements[cur_idx]
    for index, value in enumerate(list_of_elements):
        if cur_idx == len(list_of_elements)-1:
            new_list.append(now_val)
            break
        if list_of_elements[cur_idx+1] is now_val:
            cur_idx += 1
        elif list_of_elements[cur_idx+1] is not now_val:
            new_list.append(now_val)
            cur_idx += 1
            now_val = list_of_elements[cur_idx]
    return new_list


def four_point_transform(image, pts):
    # https://www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/
    # obtain a consistent order of the points and unpack them
    # individually
    rect = order_points(pts)
    (tl, tr, br, bl) = rect
    # compute the width of the new image, which will be the
    # maximum distance between bottom-right and bottom-left
    # x-coordiates or the top-right and top-left x-coordinates
    widthA = numpy.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = numpy.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = numpy.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = numpy.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    # now that we have the dimensions of the new image, construct
    # the set of destination points to obtain a "birds eye view",
    # (i.e. top-down view) of the image, again specifying points
    # in the top-left, top-right, bottom-right, and bottom-left
    # order
    dst = numpy.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype = "float32")
    # compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    # return the warped image
    return warped


def order_points(pts):
    # https://www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/
    # initialzie a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    rect = numpy.zeros((4, 2), dtype = "float32")
    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = pts.sum(axis = 1)
    rect[0] = pts[numpy.argmin(s)]
    rect[2] = pts[numpy.argmax(s)]
    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = numpy.diff(pts, axis = 1)
    rect[1] = pts[numpy.argmin(diff)]
    rect[3] = pts[numpy.argmax(diff)]
    # return the ordered coordinates
    return rect