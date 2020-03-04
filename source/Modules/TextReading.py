import cv2
import numpy
import pytesseract
from PIL import Image
from skimage import exposure
import HandyTools as HT
# https://www.pyimagesearch.com/2018/09/17/opencv-ocr-and-text-recognition-with-tesseract/
# https://www.pyimagesearch.com/2018/08/20/opencv-text-detection-east-text-detector/
# https://www.researchgate.net/publication/221786127_Natural_Scene_Text_Understanding


def tess_from_file(image_location):
    # 1) open image
    image = cv2.imread(image_location)
    texts = get_text_with_tess(image)
    return texts


def get_text_with_tess(image):
    text_list = []
    # 2) get bounding box around text
    # 2a) threshold and use open and expand to make the light area larger
    gray = exposure.rescale_intensity(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), out_range=(0,255))
    dilated = cv2.dilate(gray.copy(), None, iterations=5)
    closed = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (7,7)))
    t, thresh = cv2.threshold(closed, 200, 255, cv2.THRESH_BINARY)
    _, contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # approx = cv2.approxPolyDP(contours[0], 0.04 * cv2.arcLength(contours[0], True), True)
    for c in contours:
        min_rec_x, min_rec_y, min_rec_w, min_rec_h = cv2.boundingRect(c)
        rect_points = numpy.array([(min_rec_x, min_rec_y),
                            (min_rec_x, min_rec_y + min_rec_h),
                            (min_rec_x + min_rec_w, min_rec_y),
                            (min_rec_x + min_rec_w, min_rec_y + min_rec_h)])
        # 3) get crop of text
        text_crop = HT.four_point_transform(image, rect_points)
        # 4) threshold and binarize the text
        _, thresh = cv2.threshold(cv2.cvtColor(text_crop, cv2.COLOR_BGR2GRAY), 100, 255, cv2.THRESH_BINARY)
        # 5) use pytesseract
        pil_image = Image.fromarray(thresh)
        text = pytesseract.image_to_string(pil_image, config="-l eng --psm 9")
        text_list.append(text)
    # if meta:
    #     meta.text = [x for x in text_list if x]
    return text_list
