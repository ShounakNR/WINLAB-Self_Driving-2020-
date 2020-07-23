#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Converts directory of bagfiles into multiple data*.npz files
"""

import os
import argparse
import cv2
from PIL import Image
import rosbag
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import numpy as np

def crop_center(img):
    x,y,z = img.shape
    startx = 188
    starty = 320
    endx = 612
    endy = 560
    return img[starty:endy, startx:endx, :]

def main():
    """Extract a folder of images from a rosbag.
    """
    parser = argparse.ArgumentParser(description="Extract images from a ROS bag.")
    #parser.add_argument("bag_file", help="Input ROS bag.")
    #parser.add_argument("output_dir", help="Output directory.")
    parser.add_argument("bag_dir", help="Input directory containing bagfiles.")
    parser.add_argument("npz_dir", help="Output directory for .npz files.")
    parser.add_argument("image_topic", help="Image topic.")
    parser.add_argument("control_topic", help="Control topic.")
    args = parser.parse_args()
    bag_path = os.path.join(os.getcwd(),args.bag_dir)
    data_path = os.path.join(os.getcwd(), args.npz_dir)
    print "input directory: "+bag_path
    print "output directory: "+data_path
    filecount = 0	
    totalfiles = len([name for name in os.listdir(bag_path) if os.path.isfile(os.path.join(bag_path, name))])
    for filename in os.listdir(bag_path):
        print "Extracting from file: " +filename, "[{:.0f}%]".format(100. * filecount / totalfiles)
        bag = rosbag.Bag(os.path.join(bag_path,filename), "r")
        bridge = CvBridge()
        count = 0
        controlmsgs = []
        steerNP = []
        images=[]
        imgsNP = []
        for topic, msg, t in bag.read_messages(topics=[args.control_topic]):
            controlmsgs.append((msg.steer,t))

        for topic, msg, t in bag.read_messages(topics=[args.image_topic]):
            #print type(msg)
            cv_img = bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
            cropped_img = crop_center(cv_img)
            #print type (cropped_img)
            images.append((cropped_img,t))
            #cv2.imwrite(os.path.join(args.output_dir, "frame%06i.png" % count), cropped_img)
            #print "Wrote image %i" % count
            count += 1

        print images[0][0].shape
        #print images[0][0]
        
        img_iter=0
        for i in range(len(controlmsgs)):
            t=controlmsgs[i][1]
            valid = False
            while img_iter<len(images) and images[img_iter][1]<t:
                img_iter+=1
                valid = True
            if valid:
                imgsNP.append(images[img_iter-1][0])
                steerNP.append(controlmsgs[i][0])
                #imgsNP = np.append(imgsNP,images[img_iter-1][0],axis=0)
                #steerNP = np.append(steerNP,controlmsgs[i][0],axis=0)
                
        steerNP = np.array(steerNP)        
        imgsNP = np.array(imgsNP)
        #print steerNP.shape, imgsNP.shape 
        datafilename = "data%i.npz" % filecount
        np.savez(os.path.join(data_path, datafilename),images=imgsNP,steer=steerNP)
        print "Saving to " + datafilename
        bag.close()
        filecount+=1
    return

if __name__ == '__main__':
    main()
