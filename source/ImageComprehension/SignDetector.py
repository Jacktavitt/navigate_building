import cv2
import imutils
import os
import customImage as CIM
import pytesseract


class SignDetector:
    def __init__(self):
        pass
    
    def detect_shape(self, contour):
        shape="t(u_u)"
        peri = cv2.arcLength(contour,True)
        approx = cv2.approxPolyDP(contour, 0.04*peri, True)
        if len(approx)==3:
            shape="Triangle"
        elif len(approx)==4:
            shape = "Quadrilateral"
        elif len(approx)==5:
            shape = "Pentagon"
        else:
            shape = "Circle"
        return shape

    def detect_sign(self, image, _SHAPE):
        '''function to find the ADA signs from KU hallways.
        Args:
            image: image to look at
            _SHAPE: shape of sign we are looking for
        '''