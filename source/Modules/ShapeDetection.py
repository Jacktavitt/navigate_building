#!/usr/bin/env python3
import CustomImage
import HandyTools as HT
import numpy
from PIL import Image, ImageTk
import cv2
import os
import tkinter as tk
import string
from ImageMeta import ImageDetectionMetadata
ALL_CHARS = string.ascii_letters + string.digits


def drawSingleContour(image, c, *, text=None, color=(0, 125, 255), to_draw=True):
    '''e-z handle for cv2 implementation of calulating and drawing shape contours'''
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.04 * peri, True)
    _x, _y, _w, _h = cv2.boundingRect(c)

    M = cv2.moments(c)
    area = float(M['m00'])
    text = area if not text else text
    if area > 50 and to_draw:
        cv2.drawContours(image, [approx], -1, color, 4)
        cv2.putText(image, (f'{text}'), (_x + _w // 2, _y + _h // 2), cv2.FONT_HERSHEY_SIMPLEX, .75, color, 2)
    return area, (_w, _h), (_x, _y)


def catchWeirdShape(width, height):
    try:
        return not HT.betwixt(0.5, width / height, 2)
    except ZeroDivisionError:
        return True


def actualVsMBRArea(contour_area, minrec_area):
    '''return ratio of area of minimum bounding rectangle to contour's area
        idea is that min bounding rec should be close to contour area if it is a rectangle
    '''
    if contour_area == 0:
        return 0
    ratio = minrec_area / contour_area
    return abs(ratio)


def drawSingleMinRec(image, c, *, doop=None):
    '''draw a min bounding rectangle and return area'''
    minrec = cv2.minAreaRect(c)
    box1 = cv2.boxPoints(minrec)
    bl, tl, tr, br = box1
    height = abs(bl[1] - tl[1])
    width = abs(tl[0] - tr[0])
    weird_shape = catchWeirdShape(width, height)
    min_area = round((width * height), 2)
    box = numpy.int0(box1)
    mid = 0
    if min_area > 50 and not weird_shape:
        if doop:
            for count, item in enumerate(box):
                print(f'#{count}: {item}\n')
                cv2.circle(image, (item[0], item[1]), 10, (mid, 255 - mid, 255), 3)
                mid += 55
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        cv2.drawContours(image, [box], 0, (100, 0, 255), 2)
        cv2.putText(image, (f'area: {min_area}'), (bl[0], bl[1]), cv2.FONT_HERSHEY_SIMPLEX,
                    .75, (125, 125, 255), 2)
    return min_area, (width, height), (bl, tl, tr, br)


def drawContours(image, contours):
    for c in contours:
        drawSingleContour(image, c)


def drawBoundingBoxes(image, contours):
    areas = []
    for c in contours:
        areas.append(drawSingleMinRec(image, c))
    return areas


def calibratePlaque(source_image):
    '''sets the area and shape to expect from room marking plaques
        what we need to find is a good size to judge the pother plaques by.
    '''
    # check what we're getting
    if isinstance(source_image, CustomImage.Image):
        image = source_image
    else:
        image = CustomImage.Image(source_image)
    # remove color from image
    gray = CustomImage.Image(image, copy=True)
    gray.gray()
    gray.image = cv2.medianBlur(gray.image, 7)
    # gray.thresh(thresh_num=100)
    contours = canny_edge_and_contours(gray)
    # lets show an image of the contours, they each have a name
    # and a radio button to choose the right one
    areas = {}
    window = tk.Tk()
    window.title("Please Choose Correct Contour")
    window.configure(background='grey')

    PIXEL = tk.PhotoImage(width=1, height=1)

    listbox = tk.Listbox(window)
    listbox.pack(side='right')
    # scrollbar = tk.Scrollbar(listbox)
    # scrollbar.pack(side='right', fill='y')
    chosen = tk.StringVar()
    chosen.trace('w', simpleCallBack)

    def showChoice():
        print(chosen.get())

    def CloseWindow():
        print(f"close window!")
        if chosen.get():
            window.destroy()

    numbad = 0
    numgood = 0
    for idx, contour in enumerate(contours):
        # print(f'idx: {idx}, lencont: {len(contour)}\n')
        try:
            label = ALL_CHARS[numgood]
        except Exception as e:
            print(e)
            label = 'TILT'

        areas[idx] = {}
        areas[idx]['label'] = label
        areas[idx]['contour'] = contour
        areas[idx]['contour_area'], (areas[idx]['contour_w'], areas[idx]['contour_h']), (x, y) = drawSingleContour(image.image, contour)
        areas[idx]['minred_area'], mrwh, areas[idx]['bl_tl_tr_br'] = drawSingleMinRec(image.image, contour)
        areas[idx]['ratio'] = actualVsMBRArea(areas[idx]['contour_area'],  areas[idx]['minred_area'])

        if catchWeirdShape(areas[idx]['contour_w'],
                           areas[idx]['contour_h']) or catchWeirdShape(mrwh[0], mrwh[1]):
            areas[idx]['valid'] = False
            numbad += 1
        else:
            areas[idx]['valid'] = True
            drawSingleContour(image.image, areas[idx]['contour'], color=(255, 0, 100), text=str(label))
            if numgood % 10 == 0:
                radioholder = tk.Listbox(listbox)
                radioholder.pack(side='left')
            tk.Radiobutton(radioholder, text=label, padx=20, variable=chosen, command=showChoice, value=str(idx)).pack(side='top')
            numgood += 1

    img = Image.fromarray(image.image)
    img = ImageTk.PhotoImage(img)
    panel = tk.Label(window, image=img)
    panel.pack(side='bottom', fill='both', expand='yes')
    window.update()
    tk.Button(window, text="CONFIRM SELECTION", image=PIXEL, command=CloseWindow, compound='c', width=(image.get_width())).pack(side='top')
    window.mainloop()

    print(f"chosen item: {chosen.get()} in the result:{areas[int(chosen.get())]}")
    # print(f"just for shits: whole area dictionary: {areas}")
    return areas[int(chosen.get())]


def simpleCallBack(*args):
    print(f'variable changed {args}')


def canny_edge_and_contours(source_image, *, threshold_1=50, threshold_2=250):
    if isinstance(source_image, CustomImage.Image):
        image = source_image
    else:
        image = CustomImage.Image(source_image)
    # its edgin' time
    edged = cv2.Canny(image.image, threshold_1, threshold_2)
    # fill gaps
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    # closed = CIMAGE(cv2.morphologyEx(edged.image, cv2.MORPH_CLOSE, kernel))
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
    _, contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def get_plaques_with_hog(source_image_location, *, hog, save_directory, _debug_mode=False, use_biggest_contour=False, _fileio=True):
    '''
    source_image: CustomImage object
    good_ratio: best ratio for a plaque
    good_area: approximation of a good size for a plaque
    '''
    # open file and load it up
    image = cv2.imread(source_image_location)
    dirty_copy = image.copy()
    # print(f"image size: {image.size} from location {source_image_location}")
    if image.size < 1 or dirty_copy.size < 1:
        return []
    source_directory, source_file_name = os.path.split(source_image_location)
    # set up payload
    return_value = []
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    predictions = hog.predict(rgb_image)
    for pi, (x, y, xb, yb) in enumerate(predictions):
        # 1) for each prediction, grab the plaque image insaide. this will likely be the largest contour.
        cropped_roi = HT.crop_image(dirty_copy, x, y, xb, yb)
        # single dimension numpy array (junk)
        if cropped_roi.size < 1:
            continue
        gray = cv2.cvtColor(cropped_roi, cv2.COLOR_BGR2GRAY)
        # 2) blur and contour
        median_blur = cv2.medianBlur(gray, 9)
        contours = canny_edge_and_contours(median_blur)
        # 3) get the biggest contour
        if use_biggest_contour:
            contour_areas = [cv2.moments(c)['m00'] for c in contours]
            if not contour_areas:
                print("empty contour areas for biggest contour")
                continue
            print(f"contour areas: {contour_areas}")
            location_of_biggest = contour_areas.index(max(contour_areas)) if len(contour_areas) > 1 else 0
            big_countour = contours[location_of_biggest]
            contours = [big_countour]
        for ci, c in enumerate(contours):
            approx = cv2.approxPolyDP(c, 0.04 * cv2.arcLength(c, True), True)
            rect_points = numpy.array([x[0] for x in approx])
            payload = ImageDetectionMetadata()
            payload.image = HT.four_point_transform(cropped_roi, rect_points)
            payload.contour_area = float(cv2.moments(c)['m00'])
            payload.reference_area = None
            payload.source_image_location = source_image_location
            if _debug_mode:
                cv2.rectangle(dirty_copy, (x, y), (xb, yb), (10, 0, 225), -1)
                cv2.imshow("predicted region", dirty_copy)
                cv2.imshow("cropped area", cropped_roi)
                cv2.imshow("corrected contour", dirty_copy)
                cv2.waitKey()
                cv2.destroyAllWindows()
            if _fileio:
                payload.plaque_image_location = os.path.join(save_directory, f"{pi}_{ci}" + source_file_name)
                cv2.imwrite(payload.plaque_image_location, payload.image)
            return_value.append(payload)

    return return_value


def get_plaques_matching_ratio(source_image_location, *, save_directory, good_area, _debug_mode=False, _fileio=False):
    '''
    source_image: CustomImage object
    good_ratio: best ratio for a plaque
    good_area: approximation of a good size for a plaque
    '''
    # open file and load it up
    image = CustomImage.Image(source_image_location)
    source_directory, source_file_name = os.path.split(source_image_location)
    # set up payload
    return_value = []

    clean_copy = CustomImage.Image(image)
    dirty_copy = CustomImage.Image(image)
    gray = CustomImage.Image(image)
    gray.gray()

    # blur and threshold
    median_blur = cv2.medianBlur(gray.image, 9)
    blur_contours = canny_edge_and_contours(median_blur)
    debug_copy = dirty_copy.image.copy()
    for i, c in enumerate(blur_contours):
        # 0) get contour information
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        M = cv2.moments(c)
        contour_area = float(M['m00'])
        # 1) get minimum bounding rectangle
        min_rec_x, min_rec_y, min_rec_w, min_rec_h = cv2.boundingRect(c)
        # 2) compare that area with good area/ratio supplied to function
        ratio_good_to_maybe = min(good_area / contour_area, contour_area / good_area) if good_area != 0 and contour_area != 0 else 0
        # 3) if it is close enough, skew and crop to get proper h/w
        if ratio_good_to_maybe > .30:

            if _debug_mode:
                cv2.rectangle(debug_copy, (min_rec_x, min_rec_y), (min_rec_x + min_rec_w, min_rec_y + min_rec_h), (10, 0, 225), 2)
                cv2.putText(debug_copy, 'plaque', (min_rec_x + 5, min_rec_y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (128, 255, 0), 2)

            payload = ImageDetectionMetadata()
            rect_points = numpy.array([x[0] for x in approx])
            payload.image = HT.four_point_transform(clean_copy.image, rect_points)
            payload.contour_area = contour_area
            payload.reference_area = good_area
            payload.source_image_location = source_image_location
            if _fileio:
                payload.plaque_image_location = os.path.join(save_directory, f"{i}_" + source_file_name)
                cv2.imwrite(payload.plaque_image_location, payload.image)
            return_value.append(payload)

    if _debug_mode:
        cv2.imshow(f"points for area {contour_area}", debug_copy)
        cv2.waitKey()
        cv2.destroyWindow(f"points for area {contour_area}")

    return return_value
