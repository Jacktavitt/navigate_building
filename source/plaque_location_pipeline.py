# for running with human interaction
import argparse
import math
import timeit
import numpy
import pandas
import json
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

logging.basicConfig(format='[%(asctime)s] <%(funcName)s> : %(message)s', filename=f"run_{datetime.datetime.now().strftime('%Y-%m-%d')}.log", level=logging.INFO)
logger = logging.getLogger('wholerun')


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


def run_plaques(directory, hog):
    # 1) get value from sample calibration image
    files_to_check = HT.getFilesInDirectory(directory, '.jpg')
    logger.info(f"Looking at {len(files_to_check)} jpg images")
    results = []
    # option to use calibration
    if args['use_calibration']:
        # calib = CI.Image.open('/home/johnny/Documents/dylan_images/frame0286.jpg')
        # calib_result = SD.calibrate_run_with_plaque('/home/johnny/Documents/dylan_images/frame0286.jpg')
        # calib_result = SD.calibratePlaque(calib)
        # area = calib_result.get('contour_area')
        area = 13660.0
        logging.info(f"area from calibration: {area}")

        for f in tqdm(files_to_check, desc=f"finding plaques with area {area}"):
            results.append(SD.area_plaque_finder(
                f,
                good_area=area,
                cutoff_ratio=float(args['cutoff_ratio'])
            ))
        df = pandas.DataFrame(results)
        df.to_pickle('/home/johnny/Documents/plaque_only_testing/area_found/result_df.pkl')
    # option to use object detection
    elif args['use_hog']:
        hog_name = os.path.split(hog)[1].split('.')[0]
        hog_result = []
        detector = ObjectDetector(loadPath=hog)
        for f in tqdm(files_to_check, desc="finding plaques with HOG"):
            hog_result.append(SD.hog_plaque_finder(f, hog=detector))
        df = pandas.DataFrame(hog_result)
        df.to_pickle(f"/home/johnny/Documents/plaque_only_testing/hog_found/result_df_{hog_name}_{datetime.datetime.now().strftime('%Y-%m-%d-%s')}.pkl")


def time_hog(image):
    detector = ObjectDetector(loadPath='/home/johnny/Documents/hog_training/dylan_images/csit_hallway_detector.d')
    x = timeit.timeit(lambda: SD.roi_plaque_lean(image, hog=detector), number=1000)
    print(x)
    logging.info(f"result from runnin hog 1000 times: {x}")


def time_area(image):
    area = 13660.0
    x = timeit.timeit(lambda: SD.area_plaque_lean(image, good_area=area, cutoff_ratio=.30), number=1000)
    print(x)
    logging.info(f"result from runnin area 1000 times: {x}")


def run_text(directory):
    all_res = []
    for img in tqdm(os.listdir(directory), desc=f'running through the ringer'):
        run_res = TR.the_ringer(cv2.imread(os.path.join(directory, img)), img)
        with open('/home/johnny/Documents/text_reading_testing/ringer_raw_results_increment.json', 'a') as a:
            json.dump(run_res, a, indent=2)
        all_res.extend(run_res)
    with open('/home/johnny/Documents/text_reading_testing/ringer_raw_resutls.json', 'w') as f:
        json.dump(all_res, f, indent=2)
    df = pandas.DataFrame(all_res)
    df.to_pickle('/home/johnny/Documents/text_reading_testing/ringer_results.pkl')


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
    parser.add_argument("--plaques-only", required=False, default=False, help="run only the plaque finding part")
    parser.add_argument("-d", "--directory", required=True, help="location of images to be tested")
    parser.add_argument("-s", "--save-directory", required=False, help="where output plaque images will be saved")
    parser.add_argument("--detector", required=False, help="location of trained svm detector")
    parser.add_argument("--cutoff-ratio", required=False, default=.30, help="area ratio cutoff for calibration technique")
    parser.add_argument("-g", "--debug", required=False, default=False, type=bool, help="logger.info everything?")
    args = vars(parser.parse_args())
    logger.info(f"variables: {locals()}")
    if args.get('images_only'):
        run_text(args['directory'])
    if args.get('plaques_only'):
        run_plaques(args['directory'], args['detector'])
    else:
        main(args)
# whole plaque located in images:
# frame0034.jpg, frame0786.jpg, frame0291.jpg, frame1116.jpg, frame1255.jpg, frame0194.jpg, frame1094.jpg, frame0912.jpg, frame1100.jpg, frame1112.jpg, frame0583.jpg, frame0382.jpg, frame0894.jpg, frame0781.jpg, frame0387.jpg, frame1268.jpg, frame0677.jpg, frame0274.jpg, frame1229.jpg, frame0375.jpg, frame0886.jpg, frame0908.jpg, frame0690.jpg, frame0789.jpg, frame1114.jpg, frame0563.jpg, frame0290.jpg, frame0779.jpg, frame0007.jpg, frame1235.jpg, frame1224.jpg, frame0672.jpg, frame0691.jpg, frame0889.jpg, frame0171.jpg, frame1248.jpg, frame0189.jpg, frame1233.jpg, frame0587.jpg, frame0031.jpg, frame0287.jpg, frame0173.jpg, frame0368.jpg, frame1223.jpg, frame0805.jpg, frame0883.jpg, frame0017.jpg, frame0998.jpg, frame0570.jpg, frame0040.jpg, frame1108.jpg, frame1237.jpg, frame0878.jpg, frame0016.jpg, frame1106.jpg, frame0670.jpg, frame1245.jpg, frame0895.jpg, frame0880.jpg, frame0874.jpg, frame0014.jpg, frame0038.jpg, frame0798.jpg, frame1110.jpg, frame0584.jpg, frame0804.jpg, frame0578.jpg, frame0681.jpg, frame0284.jpg, frame0389.jpg, frame1225.jpg, frame0028.jpg, frame0033.jpg, frame0176.jpg, frame0027.jpg, frame0693.jpg, frame0696.jpg, frame0026.jpg, frame0560.jpg, frame1236.jpg, frame0273.jpg, frame1109.jpg, frame0882.jpg, frame0296.jpg, frame0873.jpg, frame1226.jpg, frame0913.jpg, frame0565.jpg, frame0802.jpg, frame0981.jpg, frame1243.jpg, frame1004.jpg, frame0906.jpg, frame0278.jpg, frame1008.jpg, frame0370.jpg, frame0184.jpg, frame0893.jpg, frame0036.jpg, frame0887.jpg, frame0582.jpg, frame0289.jpg, frame1103.jpg, frame0569.jpg, frame1119.jpg, frame0383.jpg, frame0373.jpg, frame0782.jpg, frame1220.jpg, frame1234.jpg, frame1253.jpg, frame0293.jpg, frame0682.jpg, frame0799.jpg, frame0005.jpg, frame0905.jpg, frame0988.jpg, frame0190.jpg, frame0999.jpg, frame0299.jpg, frame0200.jpg, frame0388.jpg, frame0377.jpg, frame0902.jpg, frame0020.jpg, frame1121.jpg, frame1258.jpg, frame0191.jpg, frame0788.jpg, frame0008.jpg, frame0588.jpg, frame1227.jpg, frame1257.jpg, frame0580.jpg, frame0793.jpg, frame0806.jpg, frame0792.jpg, frame0995.jpg, frame0984.jpg, frame0292.jpg, frame0006.jpg, frame1098.jpg, frame1102.jpg, frame1230.jpg, frame0281.jpg, frame0283.jpg, frame0186.jpg, frame0794.jpg, frame0371.jpg, frame0803.jpg, frame1267.jpg, frame0196.jpg, frame0043.jpg, frame0021.jpg, frame0198.jpg, frame1107.jpg, frame1216.jpg, frame0671.jpg, frame1249.jpg, frame0182.jpg, frame1222.jpg, frame0178.jpg, frame0573.jpg, frame0694.jpg, frame0378.jpg, frame0900.jpg, frame0298.jpg, frame1009.jpg, frame0898.jpg, frame0396.jpg, frame0692.jpg, frame1259.jpg, frame0897.jpg, frame0372.jpg, frame0185.jpg, frame0901.jpg, frame1006.jpg, frame0002.jpg, frame0791.jpg, frame0029.jpg, frame1001.jpg, frame0985.jpg, frame0019.jpg, frame0000.jpg, frame0384.jpg, frame0177.jpg, frame1265.jpg, frame0376.jpg, frame0892.jpg, frame1221.jpg, frame0907.jpg, frame0195.jpg, frame1003.jpg, frame0683.jpg, frame0568.jpg, frame0685.jpg, frame0993.jpg, frame1261.jpg, frame1262.jpg, frame0990.jpg, frame1002.jpg, frame0675.jpg, frame0192.jpg, frame1239.jpg, frame0571.jpg, frame0197.jpg, frame0286.jpg, frame0301.jpg, frame1240.jpg, frame0903.jpg, frame1264.jpg, frame0011.jpg, frame0386.jpg, frame1093.jpg, frame0042.jpg, frame0888.jpg, frame0911.jpg, frame0276.jpg, frame0686.jpg, frame1238.jpg, frame0899.jpg, frame0035.jpg, frame0183.jpg, frame0780.jpg, frame1242.jpg, frame0392.jpg, frame0796.jpg, frame0684.jpg, frame0022.jpg, frame0909.jpg, frame0982.jpg, frame0277.jpg, frame0797.jpg, frame0679.jpg, frame1252.jpg, frame0876.jpg, frame0175.jpg, frame1115.jpg, frame1217.jpg, frame0280.jpg, frame0787.jpg, frame0039.jpg, frame1007.jpg, frame0801.jpg, frame0881.jpg, frame0381.jpg, frame0586.jpg, frame0015.jpg, frame0024.jpg, frame1219.jpg, frame0579.jpg, frame0295.jpg, frame0676.jpg, frame1254.jpg, frame0285.jpg, frame0004.jpg, frame0023.jpg, frame1250.jpg, frame0564.jpg, frame0875.jpg, frame0170.jpg, frame0996.jpg, frame0808.jpg, frame0879.jpg, frame0991.jpg, frame0800.jpg, frame0890.jpg, frame0379.jpg, frame0689.jpg, frame1120.jpg, frame1256.jpg, frame0572.jpg, frame0910.jpg, frame0674.jpg, frame0199.jpg, frame1122.jpg, frame0374.jpg, frame0667.jpg, frame0783.jpg, frame0390.jpg, frame0687.jpg, frame0575.jpg, frame0680.jpg, frame0574.jpg, frame0012.jpg, frame1231.jpg, frame0885.jpg, frame1269.jpg, frame1113.jpg, frame0279.jpg, frame0997.jpg, frame1111.jpg, frame0181.jpg, frame1104.jpg, frame1251.jpg, frame0784.jpg, frame0795.jpg, frame0688.jpg, frame0180.jpg, frame1247.jpg, frame1263.jpg, frame0871.jpg, frame0030.jpg, frame0009.jpg, frame0994.jpg, frame0561.jpg, frame0896.jpg, frame0576.jpg, frame0041.jpg, frame1095.jpg, frame0577.jpg, frame1232.jpg, frame1101.jpg, frame0001.jpg, frame0380.jpg, frame0695.jpg, frame0003.jpg, frame0807.jpg, frame1099.jpg, frame1000.jpg, frame0172.jpg, frame1097.jpg, frame0673.jpg, frame0809.jpg, frame0193.jpg, frame1105.jpg, frame0989.jpg, frame0010.jpg, frame0397.jpg, frame0018.jpg, frame0872.jpg, frame1096.jpg, frame1215.jpg, frame1246.jpg, frame0282.jpg, frame0032.jpg, frame0393.jpg, frame1260.jpg, frame0891.jpg, frame0275.jpg, frame0188.jpg, frame1244.jpg, frame0187.jpg, frame0668.jpg, frame0179.jpg, frame0669.jpg, frame0302.jpg, frame0567.jpg, frame0566.jpg, frame0983.jpg, frame0785.jpg, frame0025.jpg, frame0300.jpg, frame0288.jpg, frame1266.jpg, frame0987.jpg, frame0810.jpg, frame1228.jpg, frame0992.jpg, frame0369.jpg, frame0585.jpg, frame0391.jpg, frame1214.jpg, frame0294.jpg, frame0884.jpg, frame0904.jpg, frame0395.jpg

# partial frame in images:
# frame0918.jpg, frame0303.jpg, frame0914.jpg, frame0778.jpg, frame0917.jpg, frame0590.jpg, frame0203.jpg, frame0919.jpg, frame1211.jpg, frame0305.jpg, frame1090.jpg, frame0366.jpg, frame0870.jpg, frame0813.jpg, frame0666.jpg, frame0304.jpg, frame0272.jpg, frame0916.jpg, frame1123.jpg, frame0980.jpg, frame0589.jpg, frame0047.jpg, frame0557.jpg, frame0398.jpg, frame0306.jpg, frame0044.jpg, frame1213.jpg, frame0367.jpg, frame0169.jpg, frame1010.jpg, frame1092.jpg, frame0869.jpg, frame0046.jpg, frame0978.jpg, frame0979.jpg, frame0812.jpg, frame0558.jpg, frame0559.jpg, frame0271.jpg, frame0399.jpg, frame0811.jpg, frame0665.jpg, frame0698.jpg, frame0204.jpg, frame0045.jpg, frame0699.jpg, frame1011.jpg, frame0168.jpg, frame1091.jpg, frame1124.jpg, frame0697.jpg, frame1212.jpg, frame0205.jpg, frame0868.jpg, frame0915.jpg, frame0206.jpg