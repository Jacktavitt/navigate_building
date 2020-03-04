# for running with human interaction
import argparse
import math
import numpy
import matplotlib.pyplot as plt
import ShapeDetection as SD
import CustomImage as CI
import HandyTools as HT
import TextReading as TR


def plot_multiple_images(results):
    labels_and_images = []
    # print(type(results), str(results))
    for f in results:
        for idx, meta in enumerate(results[f]):
            print(f"text: {meta.text}\n img: {meta.thresheld_image}")
            if meta.text and meta.thresheld_image:
                labels_and_images.append((meta.text[0], meta.thresheld_image[0]))
    numgs = len(labels_and_images)
    rows = math.ceil(math.sqrt(numgs))
    cols = math.ceil(numgs / rows)
    fig = plt.figure()
    for idx, title_img_tup in enumerate(labels_and_images):
        print(title_img_tup)
        sp = fig.add_subplot(cols, rows, idx + 1)
        plt.imshow(numpy.array(title_img_tup[1], dtype=float))
        sp.set_title(title_img_tup[0])
        sp.set_yticklabels([])
        sp.set_xticklabels([])
    fig.set_size_inches(numpy.array(fig.get_size_inches()) * numgs)
    plt.show()


def main(args):
    # 1) get value from sample calibration image
    calib = CI.Image.open(args['calibration_image'])
    # gray = CI.Image(calib, copy=True)
    # gray.gray()
    calib_result = SD.calibratePlaque(calib)
    area = calib_result.get('contour_area')
    # ratio = calib_result.get('ratio')
    width = calib_result.get('contour_w')
    height = calib_result.get('contour_h')
    bl, tl, tr, br = calib_result.get('bl_tl_tr_br')
    # 3) loop over images in a directory, outputting the names of positive and negative images
    files_to_check = HT.getFilesInDirectory(args['directory'], '.jpg')
    # TODO: below steps can be optimized with text recognition happpening over the returned list
    # we get a dict of file names, with each filename having a list of metadata
    results = {f: SD.get_plaques_matching_ratio(f,
                                                good_area=area,
                                                good_ht=height,
                                                good_wd=width,
                                                save_directory=args['save_directory'],
                                                _debug_mode=args['debug']) for f in files_to_check}
    # 4) after successfull plaque grabbing, use open and image stuff to get a bounding box around just the words, and send that to ocr
    for f in results:
        for idx, meta in enumerate(results[f]):
            results[f][idx].text, results[f][idx].thresheld_image = TR.tess_from_file(results[f][idx].plaque_image_location)
    # 5) evaluate performance for images with matching calb image and those with mismatched calibrtation image
    plot_multiple_images(results)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--calibration-image", required=True, help="image to calibrate images in directory")
    parser.add_argument("-d", "--directory", required=True, help="location of images to be tested")
    parser.add_argument("-s", "--save-directory", required=True, help="where output plaque images will be saved")
    parser.add_argument("-g", "--debug", required=False, default=False, type=bool, help="print everything?")
    # parser.add_argument("-c", "--calibration", required=True, help="image to calibrate images in directory")
    args = vars(parser.parse_args())
    print(args)
    main(args)
