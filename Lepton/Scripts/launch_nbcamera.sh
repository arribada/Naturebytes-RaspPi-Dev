#!/bin/sh
# launch_nbcamera.sh
# navigate to home directory, then to this directory, then execute python script, then back home

export PATH=/bin:/usr/bin:/usr/local/bin

cd /
cd home/pi/Naturebytes/Scripts/
python nbcamera_timelapse.py -t 30
cd /
