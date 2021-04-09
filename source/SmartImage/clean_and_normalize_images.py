# !/bin/usr/env python3
'''
must open the image
    - fill with border to make it square
    - resize to specified size (default 150)
    - save to specified directory
'''
from imutils import paths
import argparse
import cv2
import numpy as np
import os


parser = argparse.ArgumentParser()
parser.add_argument("-s", "--source_directory", required=True,
        help="directory containing images")
parser.add_argument("-o", "--output_directory", required=True,
        help="directory where augmented images will be saved")
parser.add_argument("-d", "--dimension", default=150, type=int)

if __name__=="__main__":
    args = vars(parser.parse_args())
    directory = args["source_directory"]
    counterfile = os.path.join(args["output_directory"], 'counter.txt')
    with open(counterfile) as cf:
        counter = cf.read()
    counter = int(counter)
    # print(args)
    for image_path in paths.list_images(directory):
        filename = os.path.split(image_path)[-1]
        extension = os.path.splitext(filename)[-1]
        filename = ''.join([f"{str(counter).zfill(6)}", extension])
        try:
            tmp = cv2.imread(image_path)
            if tmp is None:
                print(f"file read failed, file: {image_path}")
                continue
            img_shape = tmp.shape
            h = img_shape[0]
            w = img_shape[1]
            if h < w:
                buffer = w-h
                left = 0
                right = 0
                top = int(buffer/2)
                bottom = buffer-top
            elif w < h:
                buffer = h-w
                top = 0
                bottom = 0
                left = int(buffer/2)
                right = buffer-left
            else:
                buffer = 0
                top = 0
                left = 0
                right = 0
                bottom = 0
            # add border and save
            img = cv2.copyMakeBorder(tmp, top, bottom, left, right, cv2.BORDER_REFLECT)
            img = cv2.resize(img, (args["dimension"], args["dimension"]), interpolation=cv2.INTER_AREA)
            save_path = os.path.join(args["output_directory"], filename)
            # print(f"filename: {filename}\nimage_path: {image_path}\nsave path: {save_path}\n")
            counter += 1
            cv2.imwrite(save_path, img)

        except Exception as e:
            print(f"~~~> ERROR: {e}")
            with open(counterfile, 'w') as cf:
                cf.write(str(counter))
            continue
    with open(counterfile, 'w') as cf:
        cf.write(str(counter))

    print("~~~> DONE\n")