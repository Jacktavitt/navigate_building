#!/usr/bin/env python3
''' test efficacy of calibration system. '''
import sys
import ShapeDetection as SD
import CustomImage as CI


def main(args):
    '''do stuff'''
    image = CI.Image.open(args[1])
    return SD.calibratePlaque(image)


if __name__=='__main__':
    AREA, RATIO = main(sys.argv)
    print(f"chosen item: {RATIO}\n{AREA[int(RATIO)]}")

