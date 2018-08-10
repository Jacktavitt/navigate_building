r"""
Driver for generating hallway for better training data.
sample use: (from project root)
python source\ImageGeneration\hall_driver.py 
-d C:\Users\TJAMS002\Documents\ComputerScience\Thesis\RoomFinder\source\ImageGeneration\HALLWAYS\ -i 10
"""
import DataGenerator as DAG
import CustomImage as CIM
import cv2
import numpy as np
import os
import random
from argparse import ArgumentParser




def main(directory,images):
    IMAGE_CLASS = CIM.GeneratedImage
    IMG_GENR = DAG.ImageGenerator(IMAGE_CLASS,plaqueSize=75, resolution=10, randSeed=42)

    for n in range(int(images)):
        temp, TL, BR =IMG_GENR.make_hallway()
        temp.save(imagePath=''.join([directory,str(TL[0]),'_',str(TL[1]),'.',
                                               str(BR[0]),'_',str(BR[1]),'.',
                                               str(n),'.png']))


if __name__=='__main__':
    parser=ArgumentParser()
    parser.add_argument('--directory','-d', 
                        help = 'directory where images will be saved',
                        required=True)
    parser.add_argument('--images', '-i', 
                        help = 'how many images to make',
                        required = True)
    # parser.add_argument('--noise', '-n', 
    #                     help = 'how noisy should images be',
    #                     default=2)
    # parser.add_argument('--seed', '-s', 
    #                     default=random.randint(0,10),
    #                     help='Seed for random numbers')
    args=parser.parse_args()
    main(args.directory, args.images)