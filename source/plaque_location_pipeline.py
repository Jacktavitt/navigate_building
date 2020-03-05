# for running with human interaction
import argparse
import math
import numpy
import cv2
import matplotlib.pyplot as plt
import ShapeDetection as SD
import CustomImage as CI
import HandyTools as HT
import TextReading as TR


def plot_multiple_images(results):
    labels_and_images = []
    for meta in results:
        if meta.text and meta.thresheld_image:
            labels_and_images.extend([(meta.text[n], meta.thresheld_image[n]) for n in range(len(meta.text))])
    total_number = len(labels_and_images)
    num_imgs = 36
    num_iterations = math.ceil(total_number / num_imgs)
    # rows = math.ceil(math.sqrt(numgs))
    # cols = math.ceil(numgs / rows)
    rows = 6
    cols = 6
    for n in range(num_iterations):
        fig = plt.figure(facecolor='gray')
        for idx, title_img_tup in enumerate(labels_and_images[n * num_imgs:n * num_imgs + num_imgs]):
            # print(title_img_tup)
            sp = fig.add_subplot(cols, rows, idx + 1)
            # image = cv2.resize(title_img_tup[1], (title_img_tup[1].shape[1]//3, title_img_tup[1].shape[0]//3), interpolation=cv2.INTER_AREA)
            image = title_img_tup[1]
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
            plt.imshow(numpy.array(image, dtype=float))
            sp.set_title(title_img_tup[0])
            sp.set_yticklabels([])
            sp.set_xticklabels([])
        # fig.set_size_inches(numpy.array(fig.get_size_inches()) * numgs)
        fig.set_size_inches(numpy.array(fig.get_size_inches()) * 20)
        plt.show()
        # plt.savefig(f'/home/johnny/Documents/plaque_grab_3-4/pyplot_test/plaque_plot_simp_{n}.png')


def main(args):
    # 1) get value from sample calibration image
    if args['use_calibration']:
        calib = CI.Image.open(args['calibration_image'])
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
    results = []
    for f in files_to_check:
        results.extend(SD.get_plaques_matching_ratio(f,
                                                     good_area=area,
                                                     good_ht=height,
                                                     good_wd=width,
                                                     save_directory=args['save_directory'],
                                                     _debug_mode=args['debug']))
    # 4) after successfull plaque grabbing, use open and image stuff to get a bounding box around just the words, and send that to ocr
    for idx, meta in enumerate(results):
        results[idx].text, results[idx].thresheld_image = TR.tess_from_file(results[idx].plaque_image_location)

    # 5) evaluate performance for images with matching calb image and those with mismatched calibrtation image
    plot_multiple_images(results)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--calibration-image", required=False, help="image to calibrate images in directory")
    parser.add_argument("--use-calibration", required=True, default=False, help="image to calibrate images in directory")
    parser.add_argument("-d", "--directory", required=True, help="location of images to be tested")
    parser.add_argument("-s", "--save-directory", required=True, help="where output plaque images will be saved")
    parser.add_argument("-g", "--debug", required=False, default=False, type=bool, help="print everything?")
    # parser.add_argument("-c", "--calibration", required=True, help="image to calibrate images in directory")
    args = vars(parser.parse_args())
    print(args)
    main(args)
