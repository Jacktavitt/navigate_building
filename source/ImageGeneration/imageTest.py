import CustomImage as ci
import numpy as np
import random
import cv2


genim1 = ci.GeneratedImage(np.full((512,512,3), (120,120,120),dtype = np.uint8), color=True)
genim1.random_lines(num_lines = 13)
# genim1.show()

genim2 = ci.GeneratedImage(genim1, copy =True)
genim2.random_rectangles(num_recs=4)
# genim2.show()

genim3 = ci.GeneratedImage(genim2, copy =True)
genim3.salt_and_pepper(.03)
# genim3.show()

genim4 = ci.GeneratedImage(genim3, copy =True)
genim4.blur()
# genim4.show()

h1 = cv2.hconcat([genim1.image, genim2.image,genim3.image, genim4.image])
# h2 = cv2.hconcat([genim3.image, genim4.image])
# tot = cv2.vconcat([h1,h2])
# cv2.imshow('',tot)
# cv2.waitKey()
total = ci.GeneratedImage(h1)
total.resize(percentage=0.5)
total.show()
total.save('initial_generation_test.png')