#!/usr/bin/env python3

import os
import cv2
import argparse

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
    how to do this with functional programming ideals?
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

