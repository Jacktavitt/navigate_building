#!/usr/bin/env python3
from keras.models import load_model
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
    def __init__(self, model_location):
        img_width = 150
        img_height = 150
        try:
            if K.image_data_format() == 'channels_first':
                input_shape = (3, img_width, img_height)
            else:
                input_shape = (img_width, img_height, 3)
            # self.model = Sequential()
            # self.model.add(Conv2D(32, (3, 3), input_shape=input_shape))
            # self.model.add(Activation('relu'))
            # self.model.add(MaxPooling2D(pool_size=(2, 2)))

            # self.model.add(Conv2D(32, (3, 3)))
            # self.model.add(Activation('relu'))
            # self.model.add(MaxPooling2D(pool_size=(2, 2)))

            # self.model.add(Conv2D(64, (3, 3)))
            # self.model.add(Activation('relu'))
            # self.model.add(MaxPooling2D(pool_size=(2, 2)))

            # self.model.add(Flatten())
            # self.model.add(Dense(64))
            # self.model.add(Activation('relu'))
            # self.model.add(Dropout(0.5))
            # self.model.add(Dense(1))
            # self.model.add(Activation('sigmoid'))

            # self.model.compile(loss='binary_crossentropy',
            #             optimizer='rmsprop',
            #             metrics=['accuracy'])
            
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
        pred_string = str(result) # f"Plaque: {result[0]}\nNot Plaque: {result[1]}\n"
        cv2.putText(image.image, pred_string, (100,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (125, 250, 250), 3)
        image.show()