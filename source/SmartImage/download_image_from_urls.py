# !/usr/bin/env python3
# pulled directly from https://www.pyimagesearch.com/2018/04/09/how-to-quickly-build-a-deep-learning-image-dataset/
from imutils import paths
import argparse
import requests
import cv2
import os

ap = argparse.ArgumentParser()

ap.add_argument("-u", "--urls", required=True,
        help="path to file with image urls")
ap.add_argument("-o", "--output", required=True,
        help="directory for image file saving")
args = vars(ap.parse_args())


rows = open(args["urls"]).read().strip().split('\n')
# to remove possible dupliacte urls
rows = list(set(rows))
total = 0

# download images
for url in rows:
    try:
        req = requests.get(url, timeout=69) # hell yeah

        path = os.path.sep.join([args["output"], f"{str(total).zfill(8)}.jpg"])
        with open(path, "wb") as f:
            f.write(req.content)
        print(f"~~~> DOWNLOADED {path}")
        total += 1
    except Exception as e:
        print(f"~~~> ERROR: {e} ... SKIPPING {path}")

# now delete them if they ddo not open
for image_path in paths.list_images(args["output"]):
    delete = False
    try:
        img = cv2.imread(image_path)
        if img is None:
            delete = True
    except Exception as e:
        print(f"~~~> EXCEPTION: {e}")
        delete = True

    if delete:
        print(f"~~~> DELETING {image_path}")
        os.remove(image_path)

