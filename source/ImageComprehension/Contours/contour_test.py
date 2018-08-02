import CustomImage as CIM
import cv2
import numpy as np
from argparse import ArgumentParser
import os
'''
based on blog post by https://www.pyimagesearch.com/about/
'''
def main(filename):
    name = os.path.basename(filename)
    CIMAGE = CIM.Image
    cmage = CIMAGE.open(filename)
    cmage.resize(vertical=512)
    image = CIM.Image(cmage, copy=True)
    image.gray()
    image.blur()
    # image.show()

    # its edgin' time
    edged = CIMAGE(cv2.Canny(image.image,10,250))
    # edged.show()
    #fill gaps
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    closed = CIMAGE(cv2.morphologyEx(edged.image, cv2.MORPH_CLOSE, kernel))
    # closed.show()
    #contour time
    im2,contours,x= cv2.findContours(closed.image.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    total = 0
    isRectangle = False
    # print(str(len(contours)))
    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02*peri, True)
        if len(approx) is 4:
            cv2.drawContours(cmage.image,[approx], -1, (0,255,0), 4)
            M=cv2.moments(c)
            _x,_y,_w,_h = cv2.boundingRect(c)
            cv2.putText(cmage.image, str(M['m00']),(_x,_y),cv2.FONT_HERSHEY_SIMPLEX,.5,(255,0,125),2)
            # print("Area: {}".format(M['m00']))
            total +=1
    
    # if isRectangle: 
        # print("File {} may have a sign\n".format(filename))
        CIMAGE(cmage, copy=True).save(''.join(['snaps_with_areas/',name]))

if __name__=='__main__':
    parser=ArgumentParser()
    parser.add_argument('--file','-f', 
                        help = 'image location on disk',
                        required=True)
    args=parser.parse_args()
    main(args.file)