from PIL import Image
import sys
import os
import cv2
import CustomImage as CI
import ShapeDetection as SD
import pytesseract


def main(args):
    # directory = os.fsencode(args[1])
    for fil in os.listdir(args[1]):
        # print(fil)
        filename = args[1] + fil
        image = CI.Image.open(str(filename))
        text = SD.readPlaque(image)
        if text:
            print(f"text: {text}\nfile: {fil}")
            image.show()
        # print(text)

    # text=pytesseract.image_to_string(image.image)
    # print(text)

if __name__ == '__main__':
    main(sys.argv)