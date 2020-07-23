#!/usr/bin/env python2

import rospy
import os
import glob
import struct
import datetime
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
from torchvision.transforms import ToTensor
import time
from collections import OrderedDict
from torch.utils.data import Dataset, DataLoader,TensorDataset
from model import Net
import argparse
import cv2
from PIL import Image
import rosbag
from cv_bridge import CvBridge
from std_msgs.msg import Float32
from sensor_msgs.msg import Image
from model import Net 

class Predictor:
    def __init__(self):
        self.pub = rospy.Publisher('steer',Float32, queue_size = 1)
        self.sub = rospy.Subscriber('prius/front_camera/image_raw',Image,self.callback)
        dev = torch.device("cpu")
        self.net  = Net().to(device=dev)
        self.net.load_state_dict(torch.load("weights.pt"))
        self.net.eval()
    
    def crop_center(self,img):
        x,y,z = img.shape
        startx = 188
        starty = 320
        endx = 612
        endy = 560
        return img[starty:endy, startx:endx, :]

    def callback(self,image):
        
        bridge = CvBridge()
        cv_img = bridge.imgmsg_to_cv2(image, desired_encoding="bgr8")
        cropped_img = self.crop_center(cv_img)
        tensor_img = torch.from_numpy(cropped_img)
        t_img = torch.reshape(tensor_img,(3,424,240))
        steer_prediction = self.net.forward(t_img.unsqueeze(0))
        self.pub.publish(steer_prediction)

if __name__== "__main__":

    rospy.init_node('predictor')
    p=Predictor()
    rospy.spin()
