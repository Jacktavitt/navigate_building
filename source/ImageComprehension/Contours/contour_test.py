import CustomImage as CIM
import cv2
import numpy as np
from argparse import ArgumentParser
from ShapeDetection import markPlaque
'''
based on blog post by https://www.pyimagesearch.com/about/
'''
def main(filename):
    '''drives findPlaque now'''
    sourceImage = CIM.Image.open(filename)
    markPlaque(sourceImage)

if __name__=='__main__':
    parser=ArgumentParser()
    parser.add_argument('--file','-f', 
                        help = 'image location on disk',
                        required=True)
    args=parser.parse_args()
    main(args.file)