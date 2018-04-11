# from tut here: https://www.pyimagesearch.com/2016/02/08/opencv-shape-detection/
from shape_detector import ShapeDetector, ImageUtilities
import argparse
import imutils
import cv2

# load up argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-i","--image", required=True, help = "path to input image")
args = vars(ap.parse_args())

#preprocess image
image = cv2.imread(args["image"])
resized = ImageUtilities.resized(image, 300)
# resized= imutils.resize(image, width=300)
image = resized
ratio=image.shape[0] / float(resized.shape[0])

#gray, blur, threshold
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (3,3),0)
thresh=cv2.threshold(blurred, 60,255,cv2.THRESH_BINARY)[1]
thresh=cv2.bitwise_not(thresh)

#find contours and init shape detector
contours= cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
contours = contours[0] if imutils.is_cv2() else contours[1]
sd=ShapeDetector()

#loop over contours
for c in contours:
    # get center of c, get shape name
    M = cv2.moments(c)
    area=cv2.contourArea(c)
    print("area of contour: {}\n".format(area))
    if M["m00"] > 0 and area >300 and area <800:
        cX = int((M["m10"] / M["m00"]) * ratio)
        cY = int((M["m01"] / M["m00"]) * ratio)
        shape = sd.detect(c)

        #mutiply contour (x,y) to resize ratio, then draw shape and name
        c = c.astype("float")
        c *= ratio
        c = c.astype("int")
        cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
        cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        #show output image
        cv2.imshow("image", image)
        cv2.imshow("grey", gray)
        cv2.imshow("blur", blurred)
        cv2.imshow("thresh", thresh)
        cv2.waitKey(0)