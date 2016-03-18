## HRI DP2

This repository contains code for Human Robot Interaction Design Project Two, 
by Patrick Steadman, Tauhidur Rahman, and  Moumita Basuroychowdhury.

Adapted, updated, and amended by Chris Mavrogiannis, Jonathan Jalving, and Wil Thomason.

Prerequisites:
	Baxter robot with baxter tools on ROS Indigo
	OpenNI v1.5 (http://www.openni.ru/openni-sdk/openni-sdk-history-2/index.html)
	NITE v1.5 (http://www.openni.ru/openni-sdk/openni-sdk-history-2/index.html)
		(this must be installed on an Intel system, AMD systems do not have the proper SSSE3 instruction support)
	openni_tracker ROS package (https://github.com/ros-drivers/openni_tracker)
	ROS joystick drivers (sudo apt-get install ros-indigo-joystick-drivers)

##### To start teleoperation on Baxter:
Each step requires a new terminal window and baxter.sh to be run from ~/ros_ws

First, start the Kinect client software:

        cd ~/ros_ws
        . baxter.sh
	roslaunch openni_launch openni.launch

Launch rqt_reconfigure to enable depth registered images:

	rosrun rqt_reconfigure
	camera
	 -> driver
	    depth_registration: X

Open RVIZ to change the fixed frame base:

	rosrun rviz rviz
	Global Options
	 -> Fixed Frame: camera_depth_frame

Start the OpenNI user tracker and note the user number tracked (usually 1):

	rosrun openni_tracker openni_tracker

If a Wii Remote is being used, be sure to pair it and calibrate the gripper:

	rosrun baxter_examples gripper_keyboard.py
	C
	^c
	rosrun wiimote wiimote_node.py
	Press A & B buttons on Wiimote to pair

Enable Baxter and begin teleoperation of desired user:

	rosrun baxter_tools enable_robot.py -e
	python teleoperate_wii.py --user 1 --rate 10 --mirrored:=true

Often the tracking gets bogged down and Baxter starts making jerky motions. If this happens, kill teleoperate_wii.py and rerun the node.

Original code had a tf between camera_depth_frame and torso_1. The version of openni_tracker used here does not have these on the same tf tree.
Instead, torso_1 is a child of openni_depth_frame.
