'''moves over an image and returns chunks of it to generate 
better data.
Opens an image, calculates the size of the kernel that will
be passing over it, and then does that randomly n times.
    should also apply blur and transformation on images, returning a few images each time
    TODO: do this ^
'''
import os
import cv2
import numpy as np
import random
import CustomImage
from argparse import ArgumentParser

def apply_transformations_to(image, directory, file_name_base):
    ''' skew, rotate, flip, and bluir an image. save them all. '''
    spin_cc = image.copy()
    spin_ac = image.copy()
    skew = image.copy()
    h_blur = image.copy()
    v_blur = image.copy()
    spin_cc.rotate(10.5)
    spin_cc.rotate(-10.5)


def main(filename,percent,num,directory):
    '''driver for splitting up generated images into smaller snapshots.
    works with CustomImage Image objects.
    Args:
        filename: location of image on disk.
        percent: how much smaller than the original image each snap
            should be.
        num: how many snaps to make
        directory: where to save the snaps
    
    '''
    base = CustomImage.Image.open(filename)
    # base.resize(percentage=50)
    # base.show()
    pcnt = .01*float(percent)
    num = int(num)
    # filename has the location of the plaque baked in. This way, the generated
    # set of snapshots will be able to tell us if they actually have the numbered
    # plaque in the image.
    splitname=os.path.basename(filename).split('.')
    name=splitname[-2]
    TL=tuple([int(x) for x in splitname[0].split('_')])
    BR=tuple([int(x) for x in splitname[1].split('_')])

    y,x,_ = base.get_shape()
    width = int(x*pcnt)
    height = int(y*pcnt)

    num_with_plq=0
    # we need a safe range to allow for x and y when chopping.
    # OK x will be 0 to x - wd, y so also.
    for n in range(num):
        plaque=''
        X1=random.randint(0,x-width)
        Y1=random.randint(0,y-height)
        X2=X1+width
        Y2=Y1+height

        # now to discover if the plaque is in the image
        if X1 < TL[0] and Y1 < TL[1] and X2 > BR[0] and Y2 > BR[1]:
            plaque='_True'
            num_with_plq += 1

        crop = CustomImage.GeneratedImage(base.image[Y1:Y2,X1:X2, :])
        file_name_base = ''.join([name,'_',percent,'p_',str(n),plaque,'.png'])
        apply_transformations_to(crop, directory, file_name_base)
    
    num_without = num - num_with_plq
    if num_without > num_with_plq:
        force_with = num_without - num_with_plq
        plaque = 'True'
        for n in range(force_with):
            X1=TL[0] - 5
            Y1=TL[1] - 3*n
            X2=X1+width
            Y2=Y1+height
            crop = CustomImage.GeneratedImage(base.image[Y1:Y2,X1:X2, :])
            fname = ''.join([directory,name,'_',percent,'p_',str(n+num),plaque,'.png'])
            crop.save(fname)



if __name__=='__main__':
    parser=ArgumentParser()
    parser.add_argument('--file','-f', 
                        help = 'image location on disk',
                        required=True)
    parser.add_argument('--percent','-p', 
                        help = 'percent size of crop, ten percent would be 10.0, not 0.10',
                        required=True)
    parser.add_argument('--num','-n', 
                        help = 'number of crops to make',
                        required=True)
    parser.add_argument('--directory','-d', 
                        help = 'number of crops to make',
                        required=True)
    args=parser.parse_args()
    main(args.file,args.percent,args.num, args.directory)

