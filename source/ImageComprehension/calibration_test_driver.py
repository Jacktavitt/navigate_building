#!/usr/bin/env python3
''' test efficacy of calibration system. '''
import sys
import ShapeDetection as SD
import CustomImage as CI


def main(args):
    '''do stuff'''
    image = CI.Image.open(args[1])
    # return SD.calibratePlaque(image)
    return SD.calibrate_run_with_plaque(args[1])


if __name__=='__main__':
    result = main(sys.argv)
    # print(f"chosen item: {RATIO}\n{AREA[int(RATIO)]}")
    print(result)

