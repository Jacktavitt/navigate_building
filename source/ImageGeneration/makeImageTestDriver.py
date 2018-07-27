import DataGenerator
import CustomImage
import cv2
import numpy as np
import sys



IMAGE_CLASS = CustomImage.GeneratedImage
IMG_GENR = DataGenerator.ImageGenerator(IMAGE_CLASS, size = 512)

#create 10 each plain noise images and labelled images
noSignList = []
signList = []
for n in range(16):
    noSignList.append(IMG_GENR.make_false_image(num_randos=n))
    signList.append(IMG_GENR.make_true_image(num_randos=n))
    
good = IMAGE_CLASS.add_many(signList)
bad = IMAGE_CLASS.add_many(noSignList)

good.show()
good.save('big_good_one_2.png')

bad.show()
bad.save('big_bad_one_2.png')