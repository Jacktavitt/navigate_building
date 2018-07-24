''' This generates test data for the image capturing system.
    600 by 600 images are created and some have the correct numbered square in the image somewhere.
    others will have other shapes or noise.
'''
import random
import cv2
import numpy as np
import string
import math

class ImageGenerator(object):

    def __init__(self, IMAGECLASS, *, size = None, bgValue = None, randSeed = 42,
                plaqueValue = None, plaqueSize = None,
                fontFace = cv2.FONT_HERSHEY_SIMPLEX):
        '''initializer for generator class that produces images.
        Args:
            IMAGECLASS: the image class for objects being created.
            size: image size. 600X600 BGR by default
            bgValue: desired backgound value for image creation.
            randSeed: seed for random lines drawing.
            plaqueValue: desired color for room plaque
            plaqueSize: desired plaque size. default is a little more than 10% of image. will convert to an int
            fontFace: desired font for plaques.
        '''
        # set internal image class
        self._imgclass = IMAGECLASS
        # set up initial size
        if size is None:
            self._size = (600,600,3)
        else:
            self._size = size

        # set background value
        self._bgv = bgValue if bgValue is not None else 200
        #set random seed
        self._rands = randSeed
        random.seed(self._rands)
        #set plaque grayscale value
        self._pqv = plaqueValue if plaqueValue is not None else (50,50,50)
        #set plaque size
        if plaqueSize is None:
            self._pqs = int(math.sqrt((self._size[0]*self._size[1])*0.01))
        else:
            self._pqs = int(plaqueSize)
        #set font typeface
        self._font = fontFace
        #set font color, high contrast is key
        if len(self._pqv) is 3:
            self._fontv = tuple((n+150)%255 for n in self._pqv)
        else:
            self._fontv = (self._pqv+150)%255
        #number of chars on plaque
        self._strlen = 3
        # are we doing color for these?
        self._color = len(self._size) is 3

        print("\nDEBUG:\nBGV:{}\nPQV:{}\nPQS:{}\nFONTV:{}\nCOLOR:{}\nEND ~~"
                .format(self._bgv,self._pqv,self._pqs,self._fontv,self._color))


    def __str__(self):
        pass

    def create_canvas(self):
        '''create a base image object
        '''
        image = self._imgclass(np.full((self._size),self._bgv,np.uint8), color=self._color,seed=random.randint(0,255))
        return image


    def add_stuff(self, image, stuffScale = 2):
        '''adds other shapes and lines to image
        Args:
            image: image class instance
            stuffScale: scale of 1 to 10, how much stuff is in the image
        ''' 
        image.random_lines(seed=random.randint(0,1000),
                            num_lines = stuffScale*2)
        image.random_rectangles(seed=random.randint(0,1000),
                            num_recs = stuffScale)
        # # add lines
        # image.random_lines(seed=random.randint(0,1000), num_lines = stuffScale*2)
        # # add rectangles (full and empty)
        # image.random_rectangles(seed=random.randint(0,1000), num_recs = stuffScale)
        return image

    def _draw_room_number(self, image, x,y):
        '''Helper funciton. Draws room number/letter on the plaque.
            Args:
                self: instance
                image: image object to draw on
                (x,y): origin of plaque
        '''
        text = self._gen_plaque_text()
        # cv2.putText(img, text, origin, fontFace, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]])   
        cv2.putText(image.image, text, (x+5,y+25), self._font, 1, self._fontv, 2)
        return image

    def draw_door(self):
        '''draw a door on the image.
        '''
        pass


    def _gen_plaque_text(self):
        '''Thanks to https://stackoverflow.com/a/2257449 for the text/number generation
            generates random 3-char string of numbers and uppercase letters
        '''
        text = ''.join(random.choices(string.digits+ string.ascii_uppercase,
                         k=self._strlen))
        return text

    def draw_room_sign(self, image):
        '''places a numbered room sign somewhere on image, 
            marks filename as having room sign
            Args:
                image: image object
        '''
        #create random starting point within boundaries
        point1x = random.randint(0, (self._size[0]-self._pqs))
        point1y = random.randint(0, (self._size[0]-self._pqs))
        point2x = point1x + self._pqs
        point2y = point1y + self._pqs
        image.rectangle((point1x,point1y),(point2x,point2y),self._pqv,-1)
        image = self._draw_room_number(image, point1x, point1y)
        return image

    def make_false_image(self, num_randos=4, seasoning = 0.02, *, blur = None):
        '''generate an image without a room sign.
        Args:
            num_randos: how many random lines/recs to add
            seasoning: how much salt and pepper
            blur: optional, overrides defualt blur amount
        '''
        image = self.create_canvas()
        # image.random_lines(num_lines=num_randos, seed=random.randint(0,1000))
        # image.random_rectangles(num_recs=num_randos, seed=random.randint(0,1000))
        image = self.add_stuff(image, num_randos)
        image.salt_and_pepper(seasoning)
        if blur is not None:
            image.blur(blur)
        else:
            image.blur()
        return image

    def make_true_image(self, num_randos=4, seasoning = 0.02, *, blur = None):
        '''generate an image with a room sign.
        Args:
            num_randos: how many random lines/recs to add
            seasoning: how much salt and pepper
            blur: optional, overrides defualt blur amount
        '''
        image = self.create_canvas()
        image = self.add_stuff(image, num_randos)
        image = self.draw_room_sign(image)
        image.salt_and_pepper(seasoning)
        if blur is not None:
            image.blur(blur)
        else:
            image.blur()
        return image

