#!/usr/bin/env python3
# Custom image class wrapper to simplify image classification and parsing/ playin' around

import os
import math
import cv2
import random
import numpy as np
import CustomErrors as cerr

class Image(object):
    '''Base class for custom images. Trying hand at pythonic polymorphism.
        can initalize and save image.
    '''
    def __init__(self, image, *, path=None, fileName=None,
                 extension=None, copy=False, seed=42, color=None, percentage=None):
        '''initializer for base image class.
        Args:
            image: cv2 image or np array
            path: path to save to (default is pwd)
            fname: filename (default is temp)
            extension: filetype (default is .png)
            copy: used as token for deep copy constr
            color: let us know if we are using color or not
            percentage: for scaling, in terms of percentage of one
        '''
        if isinstance(image, Image) or copy:
            self.image = np.copy(image.image)
        elif isinstance(image, str):
            # TODO: fix path and filename stuff
            self.file_name = image
            self.image = cv2.imread(self.file_name)
        else:
            self.image = image

        self.path = '' if not path else path
        self.file_name = 'temp' if not fileName else fileName
        self.extension = 'png' if not extension else extension
        self.image_path = ''.join(self.path + self.file_name + '.' + self.extension)
        self.seed = seed
        self.percentage = percentage if percentage else 1

        self.shape = self.image.shape
        self.height = self.shape[0]
        self.width = self.shape[1]
        self.dimensions = 0 if len(self.shape) < 3 else self.shape[2]

        if self.dimensions is not 3:
            self.color = False
        else:
            self.color = True

    def copy(self):
        '''returns a Custom Image object identical to this one'''
        return Image(self.image)

    def get_size(self):
        '''returns size (height, width, dimensions) of the image'''
        return (self.height, self.width, self.dimensions)

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_dimensions(self):
        return self.dimensions

    def resize(self, *, percentage=None, vertical=None, horizontal=None):
        ''' resize image.
        Args:
            percentage: what percent size the image should be from the original
            vertical: desired vertical. horizontal will be scaled.
            horizontal: same but vis-versa
        '''
        h, w = self.image.shape[:2]

        if vertical is not None and horizontal is None:
            factor = vertical / h
        elif vertical is not None and horizontal is not None:
            self.image = cv2.resize(self.image, (vertical,horizontal), interpolation=cv2.INTER_AREA)
            return
        elif horizontal is not None and vertical is None:
            factor = horizontal / w
        elif percentage is not None:
            factor = percentage
        else:
            factor = self.percentage

        self.image = cv2.resize(self.image,None,fx=factor, fy=factor)

    def show(self, *, title = None):
        '''Show the image in a window. will wait for kill signal.'''
        title = title if title else "image"
        status = 1
        try:
            cv2.imshow(title, self.image)
            while status > 0:
                ks=cv2.waitKey(1000)
                try:
                    status = cv2.getWindowProperty(title,cv2.WND_PROP_VISIBLE)
                except Exception as e:
                    status = -1
                    break
                if ks > 0:
                    break
            cv2.destroyWindow(title)
        except Exception as e:
            print("error occured: {}",e)
            raise

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

    def thresh(self,*, type=None, thresh_num=170):
        '''simpler handle for cv2 threshold.'''
        if type == 'OTSU':
            ret2,img = cv2.threshold(self.image,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        elif not type:
            ret, img = cv2.threshold(self.image, thresh_num, 255, cv2.THRESH_BINARY)
        self.image = img

    def addColor(self):
        '''make gray image BGR compatible'''
        self.image = cv2.cvtColor(self.image, cv2.COLOR_GRAY2BGR)
        self.color = True

    def gray(self):
        '''make the image grayscale. pretty straighforward! overwrites original.'''
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.color = False

    def save(self, *, file_path=None, file_name=None, ):
        '''Saves image to file.
        '''
        if file_path:
            self.image_path = file_path
        cv2.imwrite(self.image_path, self.image)

    def blur(self, *, kernel=(3, 3), blur_type='GAUSS'):
        '''function to encapsulate blurring activity.
        Args:
            kernel: size of kernel to apply blurring
            blur_type: gaussian or average or median,
                keywords 'GAUSS', 'AVG', 'MEDIAN'
        '''
        if blur_type is 'GAUSS':
            self.image = cv2.GaussianBlur(self.image, kernel, 0)
        elif blur_type is 'AVG':
            self.image = cv2.blur(self.image, kernel)
        elif blur_type is 'MEDIAN':
            self.image = cv2.medianBlur(self.image, kernel[0])
        else:
            print("{} is not implemented. Blurring with Gauss.".format(blur_type))
            self.image = cv2.GaussianBlur(self.image, kernel, 0)

    def isolate(self, xRange, yRange):
        '''isolate section of an image.
        Args:
            xRange: tuple. grabs horiz bounds,
                i.e. 100:250
            yRange: tuple. grabs vert bounds,
                i.e. 100:250
        '''
        if len(self.image.shape) is 3:
            return self.image[xRange[0]:xRange[1], yRange[0]:yRange[1], :]
        else:
            return self.image[xRange[0]:xRange[1], yRange[0]:yRange[1]]

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
            horizStrips = []
            for i in range(0, numImages+1, x):
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

    # @classmethod
    # def show_them(cls, image_list):
    #     '''will show many image objects and wait until a key is pressed.'''
    #     try:
    #         cv2.imshow(title, self.image)
    #     except Exception as e:
    #         print(f"error occured: {e}")
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()

    @classmethod
    def open(cls, filename):
        '''simple implementation to open a file and return an image object.
        simplementation.
        '''
        try:
            img = cv2.imread(filename)
        except Exception as e:
            print(f"{e}. Filename: {filename}\n")
            raise
        
        image = cls(img)
        return image



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


    def random_rectangles(self, *, seed=None, num_recs=2):
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



