from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import cv2
import sys
import CustomImage as CI
import HandyTools as HT

class Classifier(object):
    def __init__(self, model_location):
        try:
            self.model = load_model(model_location)
        except Exception as e:
            print(f"<<<ERROR: {e}>>>")
            sys.exit(1)

    def classify_image(self, image):
        