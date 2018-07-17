# Custom image class wrapper to simplify image classification and parsing/ playin' around

import imutils
import os
import cv2
import customErrors as cerr

class Image(object):
    def __init__(self, *, imagePath=None, percentage=.25):
        ''' initialize the underlying cv2 image object.
        Args:
            self: object instance
            imagePath: path to image. must be supplied or exception will 
            be thrown to prevent onject from initializing.
            percentage: default percentage for image resizing. default is 25%
        '''
        self.imagePath = imagePath
        self.percentage = percentage

        if imagePath is None:
            raise cerr.NoImageError("No image path provided")
        else:
            try 
                self._image = cv2.imread(imagePath)
            except Exception as exc:
                print("Error encountered: {}".format(exc))
                raise

    def __str__(self):
        '''override 'str' object attribute to show some helpful info about where the image came from'''
        ps = " Default percentage is {}%".format(self.percentage) if self.percentage else ""
        return ("Image opened from {}.{}".format(self.imagePath,ps))

    def resize(self, *, percentage = None, vertical = None, horizontal = None):
        ''' resize image.
        Args:
            percentage: what percent size the image should be from the original
            vertical: desired vertical. horizontal will be scaled.
            horizontal: same but vis-versa
        '''
        h,w = cv2.shape[:2]

        if vertical and horizontal or vertical and not horizontal:
            factor = vertical / h
        elif horizontal and not vertical:
            factor = horizontal / w
        elif percentage:
            factor = percentage
        else:
            factor = self.percentage

        self._image = cv2.resize(self._image,None,fx=factor, fy=factor)

    def gray(self):
        '''make the image grayscale. pretty straighforward! overwrites original.'''
        self._image = cv2.cvtColor(self._image, cv2.COLOR_BGR2GRAY)

    def show(self):
        '''Show the image in a window. will wait for kill signal.'''
        cv2.imshow("image", self._image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
