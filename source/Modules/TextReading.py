# to run:
# python source/plaque_location_pipeline.py -c ~/Desktop/smallp.jpg -d ~/Documents/real_world_images/small_plaques -s ~/Documents/plaque_grab_3-4/simple_roi
# python source/plaque_location_pipeline.py -c ~/Desktop/smallp.jpg -d ~/Documents/real_world_images/small_plaques -s ~/Documents/plaque_grab_3-4/east_roi
import cv2
import numpy
import pytesseract
from skimage import exposure
import HandyTools as HT
import AdriansEastROIDetector as aerd
# https://www.pyimagesearch.com/2018/09/17/opencv-ocr-and-text-recognition-with-tesseract/
# https://www.pyimagesearch.com/2018/08/20/opencv-text-detection-east-text-detector/
# https://www.researchgate.net/publication/221786127_Natural_Scene_Text_Understanding


def tess_from_file(image_location):
    # 1) open image
    image = cv2.imread(image_location)
    texts, threshses = get_text_with_tess(image)
    # texts, threshses = get_text_with_aerd(image)
    return texts, threshses


def tess_from_image(source_image):
    # 1) open image
    image = source_image.copy()
    # texts, threshses = get_text_with_tess(image)
    texts, threshses = get_text_with_aerd(image)
    return texts, threshses


def get_text_with_tess(image):
    thresh_list = []
    text_list = []
    # 2) get bounding box around text
    # 2a) threshold and use open and expand to make the light area larger
    gray = exposure.rescale_intensity(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), out_range=(0, 255))
    dilated = cv2.dilate(gray.copy(), None, iterations=5)
    closed = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7)))
    t, thresh = cv2.threshold(closed, 200, 255, cv2.THRESH_BINARY)
    _, contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # approx = cv2.approxPolyDP(contours[0], 0.04 * cv2.arcLength(contours[0], True), True)
    contour_areas = [cv2.moments(c)['m00'] for c in contours]
    # print(f"contour areas: {contour_areas}")
    if not contour_areas:
        return [], []
    location_of_biggest = contour_areas.index(max(contour_areas)) if len(contour_areas) > 1 else 0
    big_countour = contours[location_of_biggest]
    # for c in contours:
    min_rec_x, min_rec_y, min_rec_w, min_rec_h = cv2.boundingRect(big_countour)
    rect_points = numpy.array([(min_rec_x, min_rec_y),
                                (min_rec_x, min_rec_y + min_rec_h),
                                (min_rec_x + min_rec_w, min_rec_y),
                                (min_rec_x + min_rec_w, min_rec_y + min_rec_h)])
    # 3) get crop of text
    # text_crop = HT.four_point_transform(image, rect_points)
    # # 4) threshold and binarize the text
    # _, thresh2 = cv2.threshold(cv2.cvtColor(text_crop, cv2.COLOR_BGR2GRAY), 100, 255, cv2.THRESH_BINARY)
    text_crop = HT.four_point_transform(gray, rect_points)
    # 4) threshold and binarize the text
    _, thresh2 = cv2.threshold(text_crop, 100, 255, cv2.THRESH_BINARY)
    # 5) use pytesseract
    # pil_image = Image.fromarray(thresh2)
    pil_image = cv2.cvtColor(thresh2, cv2.COLOR_GRAY2RGB)
    text = pytesseract.image_to_string(pil_image, config="-l eng --psm 9")
    text_list.append(text.lower())
    thresh_list.append(thresh2)

    return text_list, thresh_list


def get_text_with_aerd(image):
    # uses the east algortithm
    thresh_list = []
    text_list = []
    east = '/home/johnny/Documents/navigate_building/frozen_east_text_detection.pb'
    min_confidence = 0.5
    width = 320
    height = 320
    gray = exposure.rescale_intensity(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), out_range=(0, 255))
    rois, drawn_rois = aerd.detect_ranges_with_east(image, width, height, east, min_confidence)
    for i, (sxsy, exey, sxey, exsy) in enumerate(rois):
        # rect_points = numpy.array((sxsy, exey, sxey, exsy))
        # make the y a little bigger
        rect_points = numpy.array((
            sxsy,
            (exey[0], exey[1]+5),
            (sxey[0], sxey[1]+5),
            exsy
        ))
        text_crop = HT.four_point_transform(gray, rect_points)
        _, thresh2 = cv2.threshold(text_crop, 100, 255, cv2.THRESH_BINARY)
        # eroded = cv2.erode(thresh2, numpy.ones((7,7), numpy.uint8), iterations=1)

        # 5) use pytesseract
        pil_image = cv2.cvtColor(thresh2, cv2.COLOR_GRAY2RGB)
        inv = cv2.bitwise_not(pil_image)
        HT.showKill(thresh2, waitkey=2000)
        HT.showKill(inv, waitkey=2000)
        text = pytesseract.image_to_string(pil_image, config="-l eng --psm 9")
        # raw line
        # tex2t = pytesseract.image_to_string(pil_image, config="-l eng --psm 13")
        # etext = pytesseract.image_to_string(eroded, config="-l eng --psm 9")
        tex2t = pytesseract.image_to_string(inv, config="-l eng --psm 9")
        print(f"text {text}\nother: {tex2t}")
        text_list.append(text.lower())
        thresh_list.append(thresh2)
    return text_list, thresh_list


def get_text_with_aerd_crop_and_add(image):
    # uses the east algortithm
    thresh_list = []
    text_list = []
    east = '/home/johnny/Documents/navigate_building/frozen_east_text_detection.pb'
    min_confidence = 0.5
    width = 320
    height = 320
    gray = exposure.rescale_intensity(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), out_range=(0, 255))
    rois, drawn_rois = aerd.detect_ranges_with_east(image, width, height, east, min_confidence)
    if drawn_rois:
        HT.showKill(drawn_rois[-1], waitkey=2000)
    for i, (sxsy, exey, sxey, exsy) in enumerate(rois):
        rect_points = numpy.array((sxsy, exey, sxey, exsy))
        print(rect_points)
        # TODO: switch the trnaform to simple crop
        # text_crop = HT.four_point_transform(gray, rect_points)
        # print(sxsy[1],exey[1], sxsy[0],exey[0])
        text_crop = gray[sxsy[1]:exey[1]+5, sxsy[0]:exey[0]+5]
        # print('text_crop: ', text_crop)
        HT.showKill(text_crop, waitkey=2000)
        _, thresh2 = cv2.threshold(text_crop, 100, 255, cv2.THRESH_BINARY)

        # 5) use pytesseract
        # pil_image = cv2.cvtColor(thresh2, cv2.COLOR_GRAY2RGB)
        psmtext = pytesseract.image_to_string(text_crop, config="-l eng --psm 9")
        pslntext = pytesseract.image_to_string(text_crop)
        HT.showKill(gray, waitkey=2000)
        HT.showKill(text_crop, waitkey=2000)
        print(f"plain text: {pslntext}\npsm text: {psmtext}")
        text_list.append((pslntext.lower(), psmtext.lower()))
        thresh_list.append(text_crop)
    return text_list, thresh_list
