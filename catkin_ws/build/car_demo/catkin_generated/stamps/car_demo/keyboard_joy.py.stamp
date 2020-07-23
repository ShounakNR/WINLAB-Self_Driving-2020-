#!/usr/bin/env python

import sys, select, termios, tty
import rospy
from sensor_msgs.msg import Joy


def getKey():
    tty.setraw(sys.stdin.fileno())
    keyPress, _, _ = select.select([sys.stdin], [], [], 0.5)
    if keyPress:    
        key = sys.stdin.read(1)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        return key
    return None

if __name__== "__main__":

	settings = termios.tcgetattr(sys.stdin)
	pub = rospy.Publisher('joy', Joy, queue_size = 1)
	rospy.init_node('keyboard_joy')

	throttle_fwd = 0.0
	throttle_bwd = 0.0
	max_throttle = 1.0
	steer = 0.0
	max_right_steer =  -1.0
	max_left_steer = 1.0
	steering_sensitivity = 0.05
	throttle_sensitivity = 0.05
	steering_index = 0
	throttle_index = 4
	out_msg = Joy()
	out_msg.axes = [0.0] * 6
	out_msg.buttons = [0] * 12
	try:
		while (True):
			key = getKey()
			if (key == 'd'):
                                out_msg.axes[throttle_index] = 0.0
                                if steer <= max_right_steer:
                                    steer = -1.0
                                else:
				    steer = steer - steering_sensitivity
				out_msg.axes[steering_index] = steer

			elif (key == 'a'):
                                out_msg.axes[throttle_index] = 0.0
                                if steer >= max_left_steer:
                                    steer = 1.0
                                else:
				    steer = steer + steering_sensitivity
			 	out_msg.axes[steering_index] = steer

			elif (key == 'w'):
                                out_msg.axes[steering_index] = 0.0
				throttle_bwd = 0.0
			 	out_msg.buttons[3] = 1
                                if throttle_fwd >= max_throttle:
                                    throttle_fwd = 1.0
                                else:
                                    throttle_fwd = throttle_fwd + throttle_sensitivity
			 	out_msg.axes[throttle_index] = throttle_fwd

			elif (key == 's'):
                                out_msg.axes[steering_index] = 0.0
				throttle_fwd = 0.0
			 	out_msg.buttons[0] = 1
                                if throttle_bwd >= max_throttle:
                                    throttle_bwd = 1.0
                                else:
			 	    throttle_bwd = throttle_bwd + throttle_sensitivity
			 	out_msg.axes[throttle_index] = throttle_bwd

			elif (key == '\x20'):  # space key
			 	out_msg.buttons[1] = 1
			 	out_msg.axes[throttle_index] = -1.0

			elif (key == '\x03'): # crtl C key
				break
                        else:
                            #resets steer to 0, resets throttle to 0
                            steer = 0.0
                            out_msg.axes[throttle_index] = 0.0
                            out_msg.axes[steering_index] = steer


			pub.publish(out_msg)
			out_msg.buttons = [0] * 12

	except Exception as e:
		print(e)

	finally:
		out_msg = Joy()
		out_msg.axes = [0.0] * 6
		out_msg.buttons = [0] * 12
		pub.publish(out_msg)

		termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

