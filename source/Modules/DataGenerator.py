''' This generates test data for the image capturing system.
    600 by 600 images are created and some have the correct numbered square in the image somewhere.
    others will have other shapes or noise.
'''
import random
import cv2
import numpy as np
import string
import math
import ADA
import HandyTools as HAT

class ImageGenerator(object):

    def __init__(self, IMAGECLASS, resolution, *, size = None, bgValue = None, randSeed = 42,
                plaqueValue = None, plaqueSize = None,
                fontFace = cv2.FONT_HERSHEY_SIMPLEX):
        '''initializer for generator class that produces images.
        Args:
            IMAGECLASS: the image class for objects being created.
            resolution: how many pixels per inch (conceptually)
            size: image size. 600X600 BGR by default
            bgValue: desired backgound value for image creation.
            randSeed: seed for random lines drawing.
            plaqueValue: desired color for room plaque
            plaqueSize: desired plaque size. default is a little more than 10% of image. will convert to an int
            fontFace: desired font for plaques.
        '''
        # set internal image class
        self._imgclass = IMAGECLASS
        self.res = resolution
        # set up initial size
        if size is None:
            self._size = (600,600,3)
        else:
            self._size = size

        # set background value. default is beige.
        self._bgv = bgValue if bgValue is not None else (237,245,247)
        #set random seed
        self._rands = randSeed
        random.seed(self._rands)
        #set plaque grayscale value. default is maroon.
        self._pqv = plaqueValue if plaqueValue is not None else (42,5,102)
        #set plaque size
        if plaqueSize is None:
            self._pqs = int(math.sqrt((self._size[0]*self._size[1])*0.01))
        else:
            self._pqs = int(plaqueSize)
        #set font typeface
        self._font = fontFace
        #set font color, high contrast is key
        if len(self._pqv) is 3:
            self._fontv = tuple( HAT.hiLow255(n) for n in self._pqv)
        else:
            self._fontv = HAT.hiLow255(self._pqv)
        #number of chars on plaque
        self._strlen = 3
        # are we doing color for these?
        self._color = len(self._size) is 3

        # print("\nDEBUG:\nBGV:{}\nPQV:{}\nPQS:{}\nFONTV:{}\nCOLOR:{}\nEND ~~"
        #         .format(self._bgv,self._pqv,self._pqs,self._fontv,self._color))


    def __str__(self):
        pass

    def create_canvas(self):
        '''create a base image object
        '''
        image = self._imgclass(np.full((self._size),self._bgv,np.uint8),
                            color=self._color,seed=random.randint(0,255))
        return image

    def make_hallway(self,*, res=None,txt='358B'):
        '''Make a 'hallway' with a sign and a door. Keep the sign coordinates.
        this hallway will then be chopped up and skewed to create a better dataset.
        should be long.
            according to ADA guidelines, the baseline of raised signage should
            be between 48 and 60 inches from floor. treating 10 pixels as inches.
        Args:
            res: ratio of pixels to inches.
        Assumptions:
            Door opening is 80" by 32", 3" trim around
            Plaque height is 60" at top left corner
            plaque is 2" from door, and 7" wide/ high
            ceiling is 10'
        '''
        if res is None:
            res = self.res
        TRIM = 3
        DR_HT = (ADA.DOOR_HT +TRIM) * res
        DR_WD = (ADA.DOOR_WD+2*TRIM) * res  
        
        PQ_DIM = 8*res
        PQ_MGN = .5*res
        PQ_2_DR = 2*res
        HL_CEIL = ADA.CEIL_HT * res
        PQ_WALL_HT = HL_CEIL-(ADA.PQ_HT * res)
        HL_WD = 2*HL_CEIL
        FONT = cv2.FONT_HERSHEY_DUPLEX
        FONT_BS = 22
        # create canvas for our beautiful painting
        hallway = self._imgclass(np.full((HL_CEIL,HL_WD,3), (250,250,250),
                                dtype=np.uint8),color=self._color,
                                seed=random.randint(0,255))
        # generate text info
        # figure font size
        try:
            fontInches = ADA.get_font_size(txt, PQ_DIM/res)
        except Exception as e:
            print("ERROR: {}".format(e.message))
            raise
        FSPx=fontInches*res
        FSCALE = FSPx/FONT_BS
        # now to generate coords for the plaque
        # TODO: rn this is hardcoded. should be dynamic
        txtbx=cv2.getTextSize(txt,FONT,FSCALE,1) # get size of box bounding text
        # print("DEBUG TEXT BOX SIZE: {}".format(txtbx))
        (wt,ht),bs = txtbx
        self._pqs = wt+30 # 10px margin around at least
        Px1=random.randint(0,HL_WD-self._pqs)
        Py1= PQ_WALL_HT
        # add the plaque
        (x,y), (Px2,Py2) = self.draw_room_sign(hallway, (Px1,Py1), self._pqs)
        # add text
        self._draw_room_number(hallway, Px1, Py1+ht*2, text=txt)
        # its time for the door. will add on right if space, otherwise on left
        if Px1 < DR_WD + PQ_2_DR:
            # not enough space on left of sign
            Dx1 = Px2 + PQ_2_DR
        else:
            Dx1 = Px1 - (DR_WD+PQ_2_DR)
        Dy1 = HL_CEIL-DR_HT
        Dx2 = Dx1+DR_WD
        Dy2 = Dy1+DR_HT
        # add the door
        self.draw_door(hallway,Dx1,DW=DR_WD,DH=DR_HT)
        # a little seasoning
        hallway.salt_and_pepper()
        return hallway

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
        return image

    def _draw_room_number(self, image, x,y,*, FSCALE = 1, text = None):
        '''Helper funciton. Draws room number/letter on the plaque.
            Args:
                self: instance
                image: image object to draw on
                (x,y): origin of plaque
        '''
        if text is None:
            text = self._gen_plaque_text()
        # cv2.putText(img, text, origin, fontFace, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]])   
        cv2.putText(image.image, text, (x,y), self._font, FSCALE, self._fontv, 3)
        return image

    def draw_door(self,image, x_coord,value=(7,30,56),*,DH=None,DW=None,CH=None):
        '''draw a door on the image.
        Args:
            DH: door height
            DW: door width
            CH: ceiling height
        '''
        if DH is None:
            DH = ADA.DOOR_HT*self.res
        if DW is None:
            DW = ADA.DOOR_WD*self.res
        if CH is None:
            CH = ADA.CEIL_HT*self.res
        p1=(x_coord,(CH-DH)) # top left
        p2=(x_coord+DW,CH) # bottom right
        image.rectangle(p1,p2,value,-1)

    def _gen_plaque_text(self):
        '''Thanks to https://stackoverflow.com/a/2257449 for the text/number generation
            generates random 3-char string of numbers and uppercase letters
        '''
        text = ''.join(random.choices(string.digits+ string.ascii_uppercase,
                         k=self._strlen))
        return text

    def draw_room_sign(self, image, top_left=None, width=75):
        '''places a numbered room sign somewhere on image, 
            marks filename as having room sign
            Args:
                image: image object
                top_left: coordinates for placement of top left
                of plaque. if None, randomly place.
                    should be (point1x,point1y)
        '''
        #create random starting point within boundaries
        if top_left is not None:
            point1x,point1y = top_left
        else:
            point1x = random.randint(0, (self._size[0]-self._pqs))
            point1y = random.randint(0, (self._size[0]-self._pqs))
        point2x = point1x + width
        point2y = point1y + width
        p1 = (point1x,point1y)
        print("DEBUG point1: {}\n".format(p1))
        p2 = (point2x,point2y) 
        image.rectangle(p1,p2,self._pqv,-1)
        return p1,p2

    def make_false_image(self, num_randos=4, seasoning = 0.02, *, blur = None):
        '''generate an image without a room sign.
        Args:
            num_randos: how many random lines/recs to add
            seasoning: how much salt and pepper
            blur: optional, overrides defualt blur amount
        '''
        image = self.create_canvas()
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
        (px,py), (px2,py2) = self.draw_room_sign(image)
        image = self._draw_room_number(image, (px, py))
        image.salt_and_pepper(seasoning)
        if blur is not None:
            image.blur(blur)
        else:
            image.blur()
        return image

