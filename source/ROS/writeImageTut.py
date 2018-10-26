#!/usr/bin/env python3
"""OpenCV feature detectors with ros CompressedImage Topics in python.

This example subscribes to a ros topic containing sensor_msgs 
CompressedImage. It converts the CompressedImage into a numpy.ndarray, 
then detects and marks features in that image. It finally displays 
and publishes the new image - again as CompressedImage topic.
"""
__author__ =  'Simon Haller <simon.haller at uibk.ac.at>'
__version__=  '0.1'
__license__ = 'BSD'
# Python libs
import sys
import time
import datetime

# numpy and scipy
import numpy as np
from scipy.ndimage import filters

# OpenCV
import cv2

# Ros libraries
import roslib
import rospy

# Ros Messages
from sensor_msgs.msg import CompressedImage, Image

from cv_bridge import CvBridge, CvBridgeError

# Plaque Detection libraries
import CustomImage as CI
import ShapeDetection as SD

VERBOSE=False

class image_feature:

    def __init__(self, *, published_topic=None, subscribed_topic=None, good_ht=None, good_w=None, debug_mode=None):
        '''Initialize ros publisher, ros subscriber'''
        self.published_topic = published_topic if published_topic else "/dinkus/image/compressed"
        self.subscribed_topic = subscribed_topic if subscribed_topic else "usb_cam/image_raw/compressed"
        # must find if we are looking at compressed or raw image
        # self.is_compressed = 'compressed' in self.subscribed_topic
        self.save_date = datetime.date.today()
        # if not self.is_compressed:
        #     self.bridge = CvBridge()
        self.good_ht = good_ht
        self.good_wd = good_w
        self.x=0
        self.y=0
        self.debug_mode = debug_mode
        # published Topic
        self.image_pub = rospy.Publisher(self.published_topic, CompressedImage)
        # subscribed Topic
        # if self.is_compressed:
        self.subscriber = rospy.Subscriber(self.subscribed_topic,
                CompressedImage, self.callback, queue_size=1)
        # else:
        #     self.subscriber = rospy.Subscriber(self.subscribed_topic,
        #         Image, self.callback, queue_size=1)
        if VERBOSE:
            print(f"subscribed to {self.subscribed_topic}")


    def callback(self, ros_data):
        '''Callback function of subscribed topic.
        Here images get converted and features detected'''
        if VERBOSE:
            print('received image of type: "%s"' % ros_data.format)

        #### direct conversion to CV2 ####
        # if self.is_compressed:
        np_arr = np.fromstring(ros_data.data, np.uint8)
        image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        # else:
        #     try:
        #     # bridge = CvBridge()
        #         image_np = self.bridge.imgmsg_to_cv2(ros_data, desired_encoding="passthrough")
        #     except Exception as e:
        #         print(e)
        #         raise
        #         sys.exit(1)

        time1 = time.time()
        image_np = SD.markPlaque(CI.Image(image_np),
                                 good_ht=self.good_ht,
                                 good_wd=self.good_wd,
                                 _save=f'/home/johnny/Documents/thesis_images/crops/multi_thresh/{self.save_date}_bagrun_{time1}',
                                 _debug_mode=self.debug_mode,
                                 do_crop=True)
        # print(image_np)
        cv2.imshow('cv_img', image_np)
        cv2.waitKey(2)

        #### Create CompressedIamge ####
        # if self.is_compressed:
        msg = CompressedImage()
        msg.format = "jpeg"
        msg.data = np.array(cv2.imencode('.jpg', image_np)[1]).tostring()
        # else:
        #     msg = self.bridge.cv2_to_imgmsg(image_np, encoding="passthrough")
        # msg.header.stamp = rospy.Time.now()
        
        # Publish new image
        self.image_pub.publish(msg)
        
        #self.subscriber.unregister()

def main(calib_img, sub, pub, debug):
    '''
    calibrate plaque finder with initial image
    requires human intervention
    '''
    # calibrate image to get proper area range and ratio
        # ['label']
        # ['contour']
        # ['contour_area'], (['contour_w'], ['contour_h']) = drawSingleContour(image.image, contour)
        # ['minred_area'], mrwh = drawSingleMinRec(image.image, contour)
        # ['ratio']
    good_boy = SD.calibratePlaque(calib_img)
    good_height = good_boy['contour_h']
    good_width = good_boy['contour_w']

    
    # Initializes and cleanup ros node
    rospy.init_node('image_feature', anonymous=True)
    
    ic = image_feature(subscribed_topic=sub,
                       published_topic=pub,
                       good_ht=good_height,
                       good_w=good_width,
                       debug_mode=debug)

    try:
        rospy.spin()
    except Exception as e:
        print(f"exception occured: {e}\nExiting.")

    cv2.destroyAllWindows()

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('usage: <calibration image> <subscibing topic> <publishing topic>')
        sys.exit(1)
    elif len(sys.argv) == 5:
        debug = True
    else:
        debug = False
    main(sys.argv[1], sys.argv[2], sys.argv[3], debug)