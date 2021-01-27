# for running with human interaction
import argparse
import math
import numpy
import pandas
import pickle
import os
import datetime
from tqdm import tqdm
import cv2
import matplotlib.pyplot as plt
from tabulate import tabulate
import ShapeDetection as SD
import CustomImage as CI
import HandyTools as HT
import TextReading as TR
from ImageMeta import ImageDetectionMetadata
from detector import ObjectDetector
import logging

logging.basicConfig(format='[%(asctime)s] <%(funcName)s> : %(message)s', filename='wholerun.log', level=logging.INFO)
logger = logging.getLogger('wholerun')


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
            logger.info(title_img_tup)
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
    files_to_check = HT.getFilesInDirectory(args['directory'], '.jpg')
    logger.info(f"Looking at {len(files_to_check)} jpg images")
    results = []
    # option to use calibration
    if args['use_calibration']:
        calib = CI.Image.open(args['calibration_image'])
        calib_result = SD.calibratePlaque(calib)
        area = calib_result.get('contour_area')
        # ratio = calib_result.get('ratio')
        bl, tl, tr, br = calib_result.get('bl_tl_tr_br')
        # 3) loop over images in a directory, outputting the names of positive and negative images
        # TODO: below steps can be optimized with text recognition happpening over the returned list
        # we get a dict of file names, with each filename having a list of metadata
        for f in tqdm(files_to_check, desc=f"finding plaques with area {area}"):
            results.extend(SD.get_plaques_matching_ratio(
                f,
                good_area=area,
                save_directory=args['save_directory'],
                _debug_mode=args['debug'],
                cutoff_ratio=float(args['cutoff_ratio'])))
    # option to use object detection
    elif args['use_hog']:
        detector = ObjectDetector(loadPath=args["detector"])
        for f in tqdm(files_to_check, desc="finding plaques with HOG"):
            plaque_details_list = SD.get_plaques_with_hog(f, hog=detector, save_directory=args['save_directory'], _debug_mode=args['debug'])
            logger.debug(f"How many results for {f}: {len(plaque_details_list)}")
            results.extend(plaque_details_list)

    # 4) after successfull plaque grabbing, use open and image stuff to get a bounding box around just the words, and send that to ocr
    # for idx, meta in tqdm(enumerate(results), desc="reading text from cropped images"):
    #     results[idx].text, results[idx].thresheld_image = TR.tess_from_image(results[idx].image)

    # 5) plot the results
    # plot_multiple_images(results)
    # with open('/home/johnny/Documents/performance_metrics_3-6/hog_results.pkl', 'wb') as p:
    #     pickle.dump(results, p)
    # 6) evaluate performance for images with matching calb image and those with mismatched calibrtation image
    evaluate_performance(results)


def run_text(directory):
    # for img in tqdm(os.listdir(directory), desc="reading text from images"):
    for img in os.listdir(directory):
        # print(img)
        # pp = img.split(' ')[-1]
        # read_text, thresheld_image = TR.get_text_with_tess(cv2.imread(os.path.join(directory, img)))
        # logger.info(f"TESSERACT -> file name: {pp}\ntext read: '{read_text}'\n")
        a_r_t, _ = TR.get_text_with_aerd(cv2.imread(os.path.join(directory, img)))
        # logger.info(f"AERD -> file name: {pp}\ntext read: '{a_r_t}'\n")
        # logger.info(f"file name: {pp}\nTESS: {read_text}\nAERD: {a_r_t}")


def evaluate_performance(results):
    """
    resutls are a list of metaData objects:
        self.contour_area = 0.0
        self.reference_area = 0.0
        self.image = None
        self.thresheld_image = None
        self.text = []
        self.pose_information = None
        self.source_image_location = ''
        self.plaque_image_location = ''
        self.label = None
        self.correct_text = False
        self.other = {}
    headers = ['label', 'parsed_text', 'found_contour_area', 'ref_contour_area', 'source_image_location', 'image_has_plaque', 'plaque_found', 'text_matched', 'text_missed', 'text_misread']
    """
    with open('/home/johnny/Documents/performance_metrics_2021-01/what_are_the_results_anyway.pkl', 'wb') as f:
        pickle.dump(results, f)
    headers = ImageDetectionMetadata.headers
    results_numpy_array = numpy.array([r.to_list() for r in results])
    results_df = pandas.DataFrame(results_numpy_array, columns=headers)
    # hacky fix until we get some pose info
    # results_df['source_image_location'].apply(lambda x: float(os.path.split(x)[1].split('-')[0].replace('DSC', '0.')))
    results_df['pose_info'] = None
    results_df['TP'] = results_df.apply(lambda row: row['image_has_plaque'] is True and row['plaque_found'] is True, axis=1)
    results_df['FP'] = results_df.apply(lambda row: row['image_has_plaque'] is False and row['plaque_found'] is True, axis=1)
    results_df['TN'] = results_df.apply(lambda row: row['image_has_plaque'] is False and row['plaque_found'] is False, axis=1)
    results_df['FN'] = results_df.apply(lambda row: row['image_has_plaque'] is True and row['plaque_found'] is False, axis=1)
    TP, TN, FN, FP = results_df[['TP', 'TN', 'FN', 'FP']].sum().values
    # get precision (TP/(TP+FP))
    precision = TP / (TP + FP)
    # get recall (TP/(TP+FN))
    recall = TP / (TP + FN)
    # get f1 score (2*precision*recall)/(precision+recall)
    f1 = (2 * precision * recall) / (precision + recall)
    logger.info(
        "\nTrue Positive: %s\nTrue Negative: %s\nFalse Positive: %s\nFalse Negative: %s\nPrecision: %s\nRecall: %s\nF1: %s\n",
        TP, TN, FP, FN, precision, recall, f1
    )

    results_df.to_pickle(f'/home/johnny/Documents/performance_metrics_2021-01/hog_and_east_{datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}.pkl')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--calibration-image", required=False, help="image to calibrate images in directory")
    parser.add_argument("--use-calibration", required=False, default=False, help="image to calibrate images in directory")
    parser.add_argument("--use-hog", required=False, default=False, help="use HOG to find plaques")
    parser.add_argument("--images-only", required=False, default=False, help="run only the text from image part")

    parser.add_argument("-d", "--directory", required=True, help="location of images to be tested")
    parser.add_argument("-s", "--save-directory", required=False, help="where output plaque images will be saved")
    parser.add_argument("--detector", required=False, help="location of trained svm detector")
    parser.add_argument("--cutoff-ratio", required=False, default=.30, help="area ratio cutoff for calibration technique")
    parser.add_argument("-g", "--debug", required=False, default=False, type=bool, help="logger.info everything?")
    args = vars(parser.parse_args())
    logger.info(f"variables: {locals()}")
    if args.get('images_only'):
        run_text(args['directory'])
    else:
        main(args)
