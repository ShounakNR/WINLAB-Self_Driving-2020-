#!/usr/bin/env python

import sys, select, termios, tty
import rospy
from sensor_msgs.msg import Joy
from std_msgs.msg import Float32



class Convertor:
    def __init__(self):
    
        self.pub = rospy.Publisher('joy', Joy, queue_size = 1)
        self.sub = rospy.Subscriber('steer',Float32,self.callback)
    
    def callback(self,message):
        throttle_fwd = 0.1
        throttle_bwd = 0.0
        steer = message.data
        out_msg = Joy()
        out_msg.axes = [0.0]*6
        out_msg.axes[0]=steer
        out_msg.axes[4]=throttle_fwd
        out_msg.buttons = [0] * 12
        self.pub.publish(out_msg)
    

if __name__== "__main__":
    rospy.init_node('drive')
    c = Convertor()
    rospy.spin()

	

