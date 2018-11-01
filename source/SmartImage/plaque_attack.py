# must open saved trained moidel, look at image, and treturn classification

from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import cv2
import argparse

model = load_model('first_try.h5')
