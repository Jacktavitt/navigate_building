import dataGenerator
import customImage
import cv2
import numpy as np
import sys

if __name__ =='__main__':
    if len(sys.argv) <2:
        print("Please include desired path.")
        raise SystemExit(1)

    IMAGE_CLASS = customImage.GeneratedImage
    IMG_GENR = dataGenerator.ImageGenerator(IMAGE_CLASS)

    #create 10 each plain noise images and labelled images
    noSignList = []
    signList = []
    for n in range(10):
        noSignList.append(IMG_GENR.make_false_image())
        signList.append(IMG_GENR.make_true_image())
    