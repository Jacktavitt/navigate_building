#!/usr/bin/env python3
from keras.models import load_model
from keras.models import model_from_json
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K
import numpy as np
import cv2
import sys
import CustomImage as CI
import HandyTools as HT

class Classifier(object):
    '''
        feed it a json of a keras model, and an .h5 file of the weights
    '''
    def __init__(self, model_json, model_weights):
        img_width = 150
        img_height = 150
        try:
            if K.image_data_format() == 'channels_first':
                input_shape = (3, img_width, img_height)
            else:
                input_shape = (img_width, img_height, 3)
            
            with open(model_json) as jf:
                json_file = jf.read()

            self.model = model_from_json(json_file)
            self.model.load_weights(model_weights)
                
        except Exception as e:
            print(f"<<<ERROR: model load failed:\n{e}\n>>>")
            sys.exit(1)

    def classify_image(self, image):
        copy = CI.Image(image)
        copy.resize(vertical=150, horizontal=150)
        copy = copy.image
        copy = copy.astype("float")/255.0
        copy = img_to_array(copy)
        copy = np.expand_dims(copy, axis=0)
        try:
            result = self.model.predict(copy)
        except Exception as e:
            print(f"<<<ERROR: prediction failed:\n{e}\n>>>")
            raise
        pred_string = str(result)  # f"Plaque: {result[0]}\nNot Plaque: {result[1]}\n"
        cv2.putText(image.image, pred_string, (0,15), cv2.FONT_HERSHEY_SIMPLEX, .75, (255, 100, 250),2)
        image.show()