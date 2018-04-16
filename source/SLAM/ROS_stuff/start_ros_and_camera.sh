#!/bin/bash
echo "Starting script..."

echo "Starting roscore in the background ... "
roscore &>/dev/null &
sleep 2
echo "Now I'll run the camera in the background, in B/W ... "
rosrun usb_cam usb_cam_node  &>/dev/null &
sleep 2
echo "And run the image viewer ... "
rosrun image_view image_view image:=/usb_cam/image_raw &>/dev/null &
sleep 4
echo "She's all yours now buddy."
echo "here is the rosnode list: "
rosnode list
echo "Over and out."