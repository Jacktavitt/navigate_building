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
            print(f"<<<ERROR: {e}>>>")
            sys.exit(1)

    def classify_image(self, image):
        