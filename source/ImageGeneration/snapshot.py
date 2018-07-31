'''moves over an image and returns chunks of it to generate 
better data.
Opens an image, calculates the size of the kernel that will
be passing over it, and then does that randomly n times.
'''

import cv2
import numpy as np
import random
import CustomImage as CIM
from argparse import ArgumentParser

def main(filename,percent,num):
    base=CIM.Image.open(filename)
    # base.resize(percentage=50)
    base.show()
    pcnt = .01*float(percent)
    num = int(num)
    x,y,_ = base.get_shape()
    width = int(x*pcnt)
    height = int(y*pcnt)
    # we need a safe range to allow for x and y when chopping.
    # OK x will be 0 to x - wd, y so also.
    for n in range(num):
        X1=random.randint(0,x-width)
        Y1=random.randint(0,y-height)
        X2=X1+width
        Y2=Y1+height
        crop = CIM.Image(base.image[X1:X2,Y1:Y2, :])
        crop.show()


if __name__=='__main__':
    parser=ArgumentParser()
    parser.add_argument('--file','-f', 
                        help = 'image location on disk',
                        required=True)
    parser.add_argument('--percent','-p', 
                        help = 'percent size of crop',
                        required=True)
    parser.add_argument('--num','-n', 
                        help = 'number of crops to make',
                        required=True)
    args=parser.parse_args()
    main(args.file,args.percent,args.num)
