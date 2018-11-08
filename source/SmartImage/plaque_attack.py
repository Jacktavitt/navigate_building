# !/usr/bin/env python3
# must open saved trained moidel, look at image, and treturn classification
# python3 SmartImage/plaque_attack.py -m /home/johnny/Documents/navigate_building/source/SmartImage/first_try.h5 -d /home/johnny/Documents/navigate_building/source/ROS/images/
import argparse
from imutils import paths
import SmartFind as SF
import CustomImage as CI
from keras.models import load_model
from keras.preprocessing import image
import cv2
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--model", required=True,
        help="Trained model json file for the data")
parser.add_argument("-w", "--weights", required=True,
        help="Weights for trained model")
parser.add_argument("-d", "--image_dir", required=True,
        help="Directory of images to evaluate")
parser.parse_args()



def main(args):
    ''' tried the supplied model against the suuplied set of images '''
    model = args["model"]
    weights = args["weights"]
    image_dir = args["image_dir"]
    predictor = SF.Classifier(model, weights)
    for image in paths.list_images(image_dir):
        try:
            tmp_img = CI.Image(image)
            predictor.classify_image(tmp_img)
        except Exception as e:
            print(f"<<<ERROR: {e}>>>")


# parser = argparse.ArgumentParser()
# parser.add_argument("-m", "--model", required=True,
#         help="Trained model for the data")
# parser.add_argument("-d", "--image_dir", required=True,
#         help="Directory of images to evaluate")
# parser.parse_args()


# def main(args):
#     model = args["model"]
#     image_dir = args["image_dir"]
#     predictor = SF.Classifier(model)
#     for image in paths.list_images(image_dir):
#         try:
#             tmp_img = CI.Image(image)
#             predictor.classify_image(tmp_img)
#         except Exception as e:
#             print(f"<<<ERROR: {e}>>>")



if __name__ == "__main__":
    ARGS = vars(parser.parse_args())
    main(ARGS)