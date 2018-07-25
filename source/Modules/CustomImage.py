# Custom image class wrapper to simplify image classification and parsing/ playin' around

import os
import math
import cv2
import random
import numpy as np
import customErrors as cerr

class Image(object):
    '''Base class for custom images. Trying hand at pythonic polymorphism.
        can initalize and save image.
    '''
    def __init__(self, image, *, path='',fileName = 'temp',
                 extension = '.png', copy=False, seed = 42, color = None):
        '''initializer for base image class.
        Args:
            image: cv2 image or np array
            path: path to save to (default is pwd)
            fname: filename (default is temp)
            extension: filetype (default is .png)
            copy: used as token for deep copy constr
            color: let us know if we are using color or not
        '''
        if copy:
            self.image = np.copy(image.image)
        else:
            self.image = image
        self.imagePath = ''.join(path+fileName+extension)
        self.seed = seed
        if color is not None:
            self.color = True
        else:
            self.color = False
        # TODO: if self.image.shape is not 3:
                # self.color=False
                # else: self.color=True
        # random.seed(self.seed)

    def resize(self, *, percentage = None, vertical = None, horizontal = None):
        ''' resize image.
        Args:
            percentage: what percent size the image should be from the original
            vertical: desired vertical. horizontal will be scaled.
            horizontal: same but vis-versa
        '''
        h,w = self.image.shape[:2]

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


    def show(self, title = "image"):
        '''Show the image in a window. will wait for kill signal.'''
        try:
            cv2.imshow(title, self.image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        except Exception as e:
            print("error occured: {}",e)
            raise

    @classmethod
    def add_many(cls, image_list):
        '''creates a big image from many and shows it.
            not smart so dont make an image that is too big!
            also not smart and can only take even swquares!
        '''
        numImages = len(image_list)
        x = math.ceil(math.sqrt(numImages))
        if x == math.sqrt(numImages):
            y = int(x)
            # add images together by y
            horizStrips=[]
            for i in range(0,numImages+1,x):
                if x <= numImages:
                    horizStrips.append(cv2.hconcat([image.image for image in image_list[i:x]]))
                x = x+y
            print("\n\nDEBUG: length of horizStrips: {}\n\n".format(len(horizStrips)))
            full = cv2.vconcat([image for image in horizStrips])
            fullImage = cls(full)
            fullImage.resize(horizontal= 2048)
            return fullImage
        else:
            raise cerr.DumbProgramError("Can only accept even squares!")



    def blur(self,*, kernel = (5,5), blur_type = 'GAUSS'):
        '''function to encapsulate blurring activity.
        Args:
            kernel: size of kernel to apply blurring
            blur_type: gaussian or average or median,
                keywords 'GAUSS', 'AVG', 'MEDIAN'
        '''
        if blur_type is 'GAUSS':
            self.image = cv2.GaussianBlur(self.image,kernel, 0)
        elif blur_type is 'AVG':
            self.image = cv2.blur(self.image, kernel)
        elif blur_type is 'MEDIAN':
            self.image = cv2.medianBlur(self.image, kernel[0])
        else:
            print("{} is not implemented. Blurring with Average.".format(blur_type))
            self.image = cv2.blur(self.image, kernel)

    def rectangle(self, pt1,pt2, value = 120, thickness = 3):
        '''Draw a rectangle at coordinates
        Args:
            p1, p2: edges of rectangle
            value: greyscale value
            thickness: how thick a line. -1 for filled.
        '''
        self.image = cv2.rectangle(self.image, pt1,pt2,value, thickness)

    def line(self, pt1,pt2, value = 120, thickness = 3):
        '''Draw a line at coordinates
        Args:
            p1, p2: points of line
            value: greyscale value
            thickness: how thick a line. -1 for filled.
        '''
        self.image = cv2.line(self.image,pt1,pt2,value,thickness)

    def gray(self):
        '''make the image grayscale. pretty straighforward! overwrites original.'''
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.color = False

    def save(self, imagePath = None):
        '''Saves image to file.
        '''
        if imagePath is not None:
            self.imagePath = imagePath
        cv2.imwrite(self.imagePath, self.image)

class GeneratedImage(Image):
    '''images that are created. Inherits init from parent Image
    '''
     
    def salt_and_pepper(self, seasoning=0.007, seed = None):
        '''creates a sprinkling of salt and pepper on an image.
        Args:
            seasoning: how much salt and pepper to add
            seed: random seed
        '''
        if seed is None:
            seed = self.seed
        np.random.seed(seed)
        shapeinfo = self.image.shape
        row=shapeinfo[0]
        col=shapeinfo[1]
        s_vs_p = 0.5
        # out = np.copy(image) # don't need to make a copy, image itself is modified
        # Salt mode
        num_salt = np.ceil(seasoning * self.image.size * s_vs_p)
        coords = [np.random.randint(0, i - 1, int(num_salt))
                    for i in self.image.shape]
        self.image[coords] = 255
        # Pepper mode
        num_pepper = np.ceil(seasoning* self.image.size * (1. - s_vs_p))
        coords = [np.random.randint(0, i - 1, int(num_pepper))
                    for i in self.image.shape]
        self.image[coords] = 0

    def random_lines(self, *, seed=None, num_lines = 2):
        '''add random lines
        Args:
            seed: seed for randomint
            num_lines: how many lines to draw
        '''
        if seed is None:
            seed = self.seed
        random.seed(seed)
        for n in range(num_lines):
            pt1 = (random.randint(0, self.image.shape[0]),
                        random.randint(0, self.image.shape[1]))
            pt2 = (random.randint(0, self.image.shape[0]),
                        random.randint(0, self.image.shape[1]))            
            value = random.randint(0,255)
            if self.color:
                val2 = random.randint(0,255)
                val3 = random.randint(0,255)
                value = (value, val2, val3)
            thickness = random.randint(1,10)
            self.line(pt1,pt2,value,thickness)

    def random_rectangles(self, *, seed=None, num_recs = 2):
        '''add random rectangles
        Args:
            seed: seed for randomint
            num_lines: how many lines to draw
        '''
        if seed is None:
            seed = self.seed
        random.seed(seed)
        for n in range(num_recs):
            pt1 = (random.randint(0, self.image.shape[0]),
                        random.randint(0, self.image.shape[1]))
            pt2 = (random.randint(0, self.image.shape[0]),
                        random.randint(0, self.image.shape[1]))        
            value = random.randint(0,255)
            if self.color:
                val2 = random.randint(0,255)
                val3 = random.randint(0,255)
                value = (value, val2, val3)
            thickness = random.randint(-10,10)
            self.rectangle(pt1,pt2,value,thickness)


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

