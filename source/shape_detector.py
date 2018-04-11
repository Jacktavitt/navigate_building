import cv2
import imutils
import os

class ShapeDetector:
    def __init__(self):
        pass
    
    def detect(self, contour):
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
