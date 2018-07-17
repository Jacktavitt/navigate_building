# Custom image class wrapper to simplify image classification and parsing/ playin' around

import os
import cv2
# import Exception
import customErrors as cerr

class Image(object):
    '''Base class for custom images. Trying hand at pythonic polymorphism.
        can initalize and save image.
    '''
    def __init__(self, image, *, path='',fileName = 'temp', extension = '.png'):
        '''initializer for base image class.
        Args:
            image: cv2 image or np array
            path: path to save to (default is pwd)
            fname: filename (default is temp)
            extension: filetype (default is .png)
        '''
        self.image = image
        self.imagePath = ''.join(path+fileName+extension)

    def show(self, title = "image"):
        '''Show the image in a window. will wait for kill signal.'''
        try:
            cv2.imshow(title, self.image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        except Esception as e:
            print("error occured: {}",e)
            raise

    #TODO: add show_many that can show a list of images https://stackoverflow.com/questions/919680/can-a-variable-number-of-arguments-be-passed-to-a-function


    def save(self):
        '''Saves image to file.
        '''
        cv2.imwrite(self.imagePath, self.image)

class GeneratedImage(Image):
    '''images that are created
    '''
    pass


class ExtantImage(Image):
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
            try: 
                self.image = cv2.imread(imagePath)
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

        if vertical is not None and horizontal is not None \
                         or vertical is not None and horizontal is None:
            factor = vertical / h
        elif horizontal is not None and vertical is None:
            factor = horizontal / w
        elif percentage is not None:
            factor = percentage
        else:
            factor = self.percentage

        self.image = cv2.resize(self.image,None,fx=factor, fy=factor)

    def gray(self):
        '''make the image grayscale. pretty straighforward! overwrites original.'''
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

