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
from baxter_interface import CHECK_VERSION
from wiimote.msg import State

def get_joint_angles():
    """

    @param line: the line described in a list to process
    @param names: joint name keys
    """
    joint_angles = dict()
    joint_angles['left'] = dict()
    joint_angles['right'] = dict()

    joint_angles['left']['left_s0'] = 0.0
    joint_angles['left']['left_s1'] = 0.0
    joint_angles['left']['left_e0'] = 0.0
    joint_angles['left']['left_e1'] = 0.0
    joint_angles['left']['left_w0'] = 0.0
    joint_angles['left']['left_w1'] = 0.0
    joint_angles['left']['left_w2'] = theta
    joint_angles['right']['right_s0'] = 0.0
    joint_angles['right']['right_s1'] = 0.0
    joint_angles['right']['right_e0'] = 0.0
    joint_angles['right']['right_e1'] = 0.0
    joint_angles['right']['right_w0'] = 0.0
    joint_angles['right']['right_w1'] = 0.0
    joint_angles['right']['right_w2'] = 0.0
    
    return joint_angles

def teleoperate(rate):
    """
    Teleoperates the robot based on tf2 frames.

    @param rate: rate at which to sample joint positions in ms

    """
    rate = rospy.Rate(rate)
    # TODO: make these attributes of a class
    tfBuffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tfBuffer)

    left = baxter_interface.Limb('left')
    right = baxter_interface.Limb('right')

    while not rospy.is_shutdown():
        rate.sleep()
        wii_listen()
        joint_angles = get_joint_angles()
        print joint_angles
        if joint_angles is not None:
            left.set_joint_positions(joint_angles['left'])
            right.set_joint_positions(joint_angles['right'])
            operate_gripper()
            print "updated positions"
    print "Rospy shutdown, exiting loop."
    return True

def wii_listen():
    #rospy.init_node('listener', anonymous=False)
    rospy.Subscriber('/wiimote/state', State , wiimote_state_callback)

def wiimote_state_callback(state_data):
    global theta
    global B_button
    gx = state_data.linear_acceleration_zeroed.x
    gz = state_data.linear_acceleration_zeroed.z
    
    theta = math.atan2(gx,gz)
    B_button = state_data.buttons[5]


def operate_gripper():
    #left = baxter_interface.Gripper('left', CHECK_VERSION)
    left_grip = baxter_interface.Gripper('left', CHECK_VERSION)
    if B_button: 
       print 'button B pressed'
       left_grip.close()
    else:
       left_grip.open()
       print "button B released"


def main():
    rate = 20
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

def defGlobals():
    global theta
    global B_button
    B_button = False
    theta = 0.0

if __name__ == '__main__':
    defGlobals()
    main()
