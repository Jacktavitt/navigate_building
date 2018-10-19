'''simple driver to test plaque calibration'''
#!/usr/bin/env python3

import cv2
import sys
import numpy as np
import CustomImage as CI
import HandyTools as HT
import ShapeDetection as SD


def main(args):
    '''runs the driver '''
    calib = CI.Image.open(args[1])
    copy = CI.Image(calib, copy=True)
    gray = CI.Image(copy, copy=True)

    SD.calibratePlaque(gray)

if __name__ == '__main__':
    main(sys.argv)
