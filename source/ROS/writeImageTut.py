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
import sys, time

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

    def __init__(self, *, publishedTopic=None, subscribedTopic=None, save_date='12-31-1999'):
        '''Initialize ros publisher, ros subscriber'''
        self.publishedTopic = publishedTopic if publishedTopic else "/dinkus/image/compressed"
        self.subscribedTopic = subscribedTopic if subscribedTopic else "usb_cam/image_raw/compressed"
        # must find if we are looking at compressed or raw image
        self.is_compressed = 'compressed' in self.subscribedTopic
        self.save_date = save_date
        if not self.is_compressed:
            self.bridge = CvBridge()
        self.x=0
        self.y=0
        # published Topic
        self.image_pub = rospy.Publisher(self.publishedTopic, CompressedImage)
        # subscribed Topic
        if self.is_compressed:
            self.subscriber = rospy.Subscriber(self.subscribedTopic,
                CompressedImage, self.callback, queue_size=1)
        else:
            self.subscriber = rospy.Subscriber(self.subscribedTopic,
                Image, self.callback, queue_size=1)
        if VERBOSE:
            print(f"subscribed to {self.subscribedTopic}")


    def callback(self, ros_data):
        '''Callback function of subscribed topic.
        Here images get converted and features detected'''
        if VERBOSE:
            print('received image of type: "%s"' % ros_data.format)

        #### direct conversion to CV2 ####
        if self.is_compressed:
            np_arr = np.fromstring(ros_data.data, np.uint8)
            image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        else:
            try:
            # bridge = CvBridge()
                image_np = self.bridge.imgmsg_to_cv2(ros_data, desired_encoding="passthrough")
            except Exception as e:
                print(e)
                raise
                sys.exit(1)

        time1 = time.time()
        image_np = SD.markPlaque(CI.Image(image_np), 0.11, 3737, _save=f'{self.save_date}_bagrun_{time1}')
        # print(image_np)
        cv2.imshow('cv_img', image_np)
        cv2.waitKey(2)

        #### Create CompressedIamge ####
        if self.is_compressed:
            msg = CompressedImage()
            msg.format = "jpeg"
            msg.data = np.array(cv2.imencode('.jpg',  image_np)[1]).tostring()
        else:
            msg = self.bridge.cv2_to_imgmsg(image_np, encoding="passthrough")
        # msg.header.stamp = rospy.Time.now()
        
        # Publish new image
        self.image_pub.publish(msg)
        
        #self.subscriber.unregister()

def main(args):
    '''Initializes and cleanup ros node'''
    rospy.init_node('image_feature', anonymous=True)
    print(args)
    if len(args) is 4:
        ic = image_feature(subscribedTopic=args[1], publishedTopic=args[2], save_date=args[3])
    elif len(args) is 3:
        ic = image_feature(subscribedTopic=args[1], publishedTopic=args[2])
    else:
        ic = image_feature()
    try:
        rospy.spin()
    except Exception as e:
        print(f"exception occured: {e}\nExiting.")
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)