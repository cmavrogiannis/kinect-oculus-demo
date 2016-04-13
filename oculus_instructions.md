# Instructions for Oculus Setup

This document contains the instructions for running the Oculus component of the 
Baxter teleoperation demo.

## Steps

1. Select a computer with an NVidia graphics card.
2. With the computer turned **off**, connect the Oculus to the computer.
  - Connect to the HDMI and USB ports on the computer
  - Connect both webcams to the computer
  - Plug the Oculus power adapter in
3. Boot the computer.
4. Once booted, check the NVidia X config and verify that both X Screen 0 and X 
   Screen 1 are present on the left side.
     If they are not, go to the screen config tab, set the Oculus to use a new X
     screen, save the X config, and restart the computer.
5. Install metacity, git, cmake, ninja-build, a C++ compiler, GLEW, GLFW, and OpenCV
6. With the Oculus on X Screen 1, run `run-oculus.sh` (a script in this 
   directory). The script will start the Oculus service, configure the display, 
   and build and run the demo.
