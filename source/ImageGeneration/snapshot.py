'''moves over an image and returns chunks of it to generate 
better data.
Opens an image, calculates the size of the kernel that will
be passing over it, and then does that randomly n times.
    should also apply blur and transformation on images, returning a few images each time
    TODO: do this ^
'''
import os
import cv2
import random
from argparse import ArgumentParser

def apply_transformations_to(image, directory, file_name_base):
    ''' skew, rotate, flip, and bluir an image. save them all. '''
    spin_cc = image.copy()
    spin_ac = image.copy()
    skew = image.copy()
    h_blur = image.copy()
    v_blur = image.copy()
    spin_cc.rotate(10.5)
    spin_ac.rotate(-10.5)
    spin_cc.save()


def main(filename, winsize, num, directory):
    '''driver for splitting up generated images into smaller snapshots.
    Args:
        filename: location of image on disk.
        percent: how much smaller than the original image each snap
            should be.
        num: how many snaps to make
        directory: where to save the snaps
    '''
    base = cv2.imread(filename)
    base_height, base_width, _ = base.shape
    # filename has the location of the plaque baked in. This way, the generated
    # set of snapshots will be able to tell us if they actually have the numbered
    # plaque in the image.
    splitname = os.path.basename(filename).split('.')
    name = splitname[-2]
    TL = tuple([int(x) for x in splitname[0].split('_')])
    BR = tuple([int(x) for x in splitname[1].split('_')])
    # first make some that have the plaque in it
    x_limit = TL[0] if TL[0] <= base_width - winsize else base_width - winsize
    y_limit = TL[1] if TL[1] <= base_width - winsize else base_width - winsize
    x1_list = random.choices(range(max(0, BR[0] - winsize), x_limit), k=num)
    y1_list = random.choices(range(max(0, BR[1] - winsize), y_limit), k=num)
    for x, y in zip(x1_list, y1_list):
        crop = base[y:y + winsize, x:x + winsize, :].copy()
        file_name_base = os.path.join(directory, f"{winsize}_{name}_{x}_{y}_true.png")
        cv2.imwrite(file_name_base, crop)

    # now lets make some without plaque in it
    left_of_plaque = list(range(0, TL[0] - winsize)) if TL[0] >= winsize else []
    right_of_plaque = list(range(BR[0], base_width - winsize)) if base_width >= winsize else []
    valid_tl_x = left_of_plaque + right_of_plaque
    x1_list_neg = random.choices(valid_tl_x, k=num)
    y1_list_neg = random.choices(range(base_height - winsize), k=num)
    for x, y in zip(x1_list_neg, y1_list_neg):
        crop = base[y:y + winsize, x:x + winsize, :].copy()
        file_name_base = os.path.join(directory, f"{winsize}_{name}_{x}_{y}_false.png")
        cv2.imwrite(file_name_base, crop)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--source_directory', '-s',
                        help='directory of images to snapshot',
                        required=True)
    parser.add_argument('--winsize', '-w',
                        help='pixel size of window',
                        required=True)
    parser.add_argument('--num', '-n',
                        help='number of crops to make',
                        required=True)
    parser.add_argument('--directory', '-d',
                        help='number of crops to make',
                        required=True)
    args = parser.parse_args()
    for filename in os.listdir(args.source_directory):
        main(
            os.path.join(args.source_directory, filename),
            int(args.winsize),
            int(args.num),
            args.directory
        )
