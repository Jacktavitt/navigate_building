import os
import cv2

def getFilesInDirectory(directory,fileType):
    fileList=[]
    for item in os.listdir(directory):
        if item.lower().endswith(fileType):
            fileList.append("{}{}".format(directory,item))
    return fileList

def hiLow255(num):
    return 0 if num > 122 else 255