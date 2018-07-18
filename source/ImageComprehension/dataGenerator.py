''' This generates test data for the image capturing system.
    600 by 600 images are created and some have the correct numbered square in the image somewhere.
    others will have other shapes or noise.
'''
import random
import cv2
import numpy as np

class ImageGenerator(object):

    def __init__(self, IMAGECLASS, *, size = None, bgValue = None, randSeed = 42,
                plaqueValue = 100, plaqueSize = 70,
                fontFace = cv2.FONT_HERSHEY_SIMPLEX):
        '''size argument will take a tuple or a single number for
            defualt size
        '''
        # set internal image class
        self._imgclass = IMAGECLASS
        # set up initial size
        if size is None:
            self._size = (600,600)
        elif type(size) is not tuple:
            self._size = (size,size)
        elif len(size is not 2):
            self._size = (size[0],size[0])
        else:
            self._size = size

        # set background value
        self._bgv = bgValue if bgValue is not None else 200
        #set random seed
        self._rands = randSeed
        #set plaque grayscale value
        self._pqv = plaqueValue
        #set plaque size
        self._pqs = plaqueSize
        #set font typeface
        self._font = fontFace
        #set font color, high contrast is key
        self._fontv = (self._pqv+150)%255
        #number of chars on plaque
        self._strlen = 3


    def __str__(self):
        pass

    def _create_canvas(self, greyValue):
        img = self._imgclass(np.full((self._size),greyValue,np.uint8))
        return img

    def draw_base_image(self):
        '''Draws base image, wrapped in custome liner
            optionally adding random other shapes and noise
        '''
        img = self._create_canvas(200)
        # light grey background
        # Must reference image's .image object or it wont work
        # now add noise and other shapes and lines
        img = self.add_noise(img)
        return img

    def _draw_room_number(self, image, x,y):
        '''Helper funciton. Draws room number/letter on the plaque.
            Args:
                self: instance
                image: image to draw on
                (x,y): origin of plaque
        '''
        text = self._gen_plaque_text(self)
        # cv2.putText(img, text, origin, fontFace, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]])   
        cv2.putText(image, text, (x,y+20), self._font, 1, self._fontv, 2)
        return image

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
        '''
        #create random starting point within boundaries
        point1x = random.randint(0, (self._size[0]-self._pqs))
        point1y = random.randint(0, (self._size[0]-self._pqs))
        point2x = point1x + self._pqs
        point2y = point1y + self._pqs
        image = cv2.rectangle(image, (point1x,point1y),(point2x,point2y),(self._pqv),-1)
        image = self._draw_room_number(image, point1x, point1y)
        return image

    def make_false_image(self):
        img = self.draw_base_image()
        return img

    def make_true_image(self):
        img = self.draw_base_image()
        img.image = self.draw_room_sign(img.image)
        return img
