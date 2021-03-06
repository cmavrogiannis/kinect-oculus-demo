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

theta = 0.5
   
def wiimote_state_callback(state_data):
    gx = state_data.linear_acceleration_zeroed.x
    gz = state_data.linear_acceleration_zeroed.z
    print gx, gz    
    global theta
    theta = math.atan2(gx,gz)

def wii_wrist_roll():
    #rospy.init_node('listener',anonymous=False)
    rospy.Subscriber('/wiimote/state', State, wiimote_state_callback)
    wrist_roll = theta
    return wrist_roll

def main():

    arg_fmt = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(formatter_class=arg_fmt,
                                     description=main.__doc__)
    parser.add_argument(
        '-r', '--rate', type=int, default=10,
        help='rate to sample the joint positions'
    )

    args = parser.parse_args(rospy.myargv()[1:])

    print("Initializing node... ")
    rospy.init_node("wii_wrist_roll")
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

    while not rospy.is_shutdown(): 
        wrist_ang = wii_wrist_roll()
        joint_angles = dict()
        joint_angles['left'] = dict()
        joint_angles['right'] = dict()
        left = baxter_interface.Limb('left')
        right = baxter_interface.Limb('right')
        rate = 20
        rate = rospy.Rate(rate)

        rate.sleep()
        tfBuffer = tf2_ros.Buffer()
        listener = tf2_ros.TransformListener(tfBuffer)

        joint_angles['left']['left_w2'] = wrist_ang

        left.set_joint_positions(joint_angles['left'])
        print joint_angles['left']
        return True

if __name__ == '__main__':
    main()
