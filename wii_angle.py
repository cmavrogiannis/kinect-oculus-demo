#!/usr/bin/env python

"""
Human Robot Interation, Design Project II
"""
import argparse
import sys

import rospy
import tf2_ros
import math
import numpy as np

import baxter_interface
import baxter_external_devices
from baxter_interface import CHECK_VERSION
#from wiimote.msg import State
from wiimote.msg import State

def wiimote_state_callback(state_data):
	gx = state_data.linear_acceleration_zeroed.x
	gz = state_data.linear_acceleration_zeroed.z
	theta = math.atan2(gx,gz)
	#print 'theta = ', theta
	
	#if state_data.buttons[5]: 
	#	print 'button B pressed'
	#	left.close
	#else:
	#	left.open
	left.set_joint_positions(joint_angles['left']['left_w2'])
		

def teleoperate(rate):
	"""
	Teleoperates the robot based on tf2 frames.

	@param rate: rate at which to sample joint positions in ms

	"""
	#rate = rospy.Rate(rate)

	tfBuffer = tf2_ros.Buffer()
	listener = tf2_ros.TransformListener(tfBuffer)
	joint_angles = dict()
	joint_angles['left'] = dict()
	joint_angles['right'] = dict()

	left = baxter_interface.Limb('left')
	right = baxter_interface.Limb('right')
	wrist_roll_angle = wii_listen()
	joint_angles['left']['left_w2'] = wrist_roll_angle
	while not rospy.is_shutdown():
		rate.sleep()
		#joint_angles = get_joint_angles(user, tfBuffer, test, mirrored)
		#if joint_angles is not None:
		#left.set_joint_positions(joint_angles['left']['left_w2'])
		print "updated positions"
	print "Rospy shutdown, exiting loop."
	return True


def wii_listen():
	rospy.init_node('listener', anonymous=False)
	rospy.Subscriber('/wiimote/state', State , wiimote_state_callback)
	
	rospy.spin()
	
def main():
	rate = 10
	print("Initializing node... ")
	rospy.init_node("teleoperation")
	print("Getting robot state... ")
	rs = baxter_interface.RobotEnable(CHECK_VERSION)
	init_state = rs.state().enabled

	def clean_shutdown():
		print("\nExiting...")
		if not init_state:
			print("Disabling robot...")
			rs.disable()
	rospy.on_shutdown(clean_shutdown)

	print("Enabling robot... ")
	rs.enable()
	teleoperate(rate)


if __name__ == '__main__':
	main()
