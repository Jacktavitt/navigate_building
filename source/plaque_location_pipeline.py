# for running with human interaction
import argparse
import ShapeDetection as SD
import HandyTools as HT


def main(args)
    # 1) get value from sample calibration image
    calib = CI.Image.open(args['calibration'])
    gray = CI.Image(calib, copy=True)
    gray.gray()
    calib_result = SD.calibratePlaque(gray)
    area = calib_result.get('contour_area')
    ratio = calib_result.get('ratio')
    width = calib_result.get('contour_w')
    height = calib_result.get('contour_h')
    bl, tl, tr, br = calib_result.get('bl_tl_tr_br')
    # 2) output cropped image to OCR step

    # 3) loop over images in a directory, outputting the names of positive and negative images
    files_to_check = HT.getFilesInDirectory(args['directory'], '.jpg')
    results = {f: do_thing(f) for f in files_to_check}

    # TODO: after successfull plaque grabbing, use open and image stuff to get a bounding box around just the words, and send that to ocr
    # 4) evaluate performance for images with matching calb image and those with mismatched calibrtation image

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--calibration", required=True, help="image to calibrate images in directory")
    parser.add_argument("-d", "--directory", required=True, help="location of images to be tested")
    # parser.add_argument("-c", "--calibration", required=True, help="image to calibrate images in directory")
    args = vars(parser.parse_args())