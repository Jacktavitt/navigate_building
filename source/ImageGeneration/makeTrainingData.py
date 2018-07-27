"""
Driver for generating training and test data for the Image Comprehesion
aspect of the room navigator.
"""
import DataGenerator
import CustomImage
import cv2
import numpy as np
import os
import random
from argparse import ArgumentParser




def main(directory, seed, images, noise):
    IMAGE_CLASS = CustomImage.GeneratedImage
    IMG_GENR = DataGenerator.ImageGenerator(IMAGE_CLASS, size = (512,512,3),
                                            randSeed = int(seed),plaqueSize=75)
    for i in range(0,int(images)):
        bi=IMG_GENR.make_false_image(num_randos=int(noise))
        gi=IMG_GENR.make_true_image(num_randos=int(noise))
        ps = ''.join([directory,str(i)])
        bi.save(imagePath=''.join([ps,'.png']))
        gi.save(imagePath=''.join([ps,'_pos.png']))


if __name__=='__main__':
    parser=ArgumentParser()
    parser.add_argument('--directory','-d', 
                        help = 'directory where images will be saved',
                        required=True)
    parser.add_argument('--images', '-i', 
                        help = 'how many images to make',
                        required = True)
    parser.add_argument('--noise', '-n', 
                        help = 'how noisy should images be',
                        default=2)
    parser.add_argument('--seed', '-s', 
                        default=random.randint(0,10),
                        help='Seed for random numbers')
    args=parser.parse_args()
    main(args.directory, args.seed , args.images, args.noise)