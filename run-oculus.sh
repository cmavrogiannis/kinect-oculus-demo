#/bin/bash

echo "Fetching dependencies:"

if [ ! -d "OculusRiftInAction" ]; then
  echo -e "\tFetching Oculus Example Code:"
  git clone --recursive https://github.com/OculusRiftInAction/OculusRiftInAction 2>&1 | awk '{print "\t\t" $0}'
fi

echo "Building dependencies:"

echo -e "\tBuilding examples:"
cd OculusRiftInAction
cp ../modified-demo.cpp examples/cpp/opencv/Example_13_4_StereoWebcamDemo.cpp
mkdir -p build
cd build
cmake -G Ninja .. | awk '{print "\t\t" $0}'
ninja | awk '{print "\t" $0}'
cd ../..

echo "Running service:"
./OculusRiftInAction/libraries/OculusSDK/Service/OVRServer/Bin/Linux/x86_64/ReleaseStatic/ovrd &

echo "Running metacity:"
DISPLAY=:0.1 metacity &

echo "Running demo"
trap 'kill $(jobs -p)' EXIT
Display=:0.1 ./OculusRiftInAction/build/output/Example_13_4_StereoWebcamDemo
