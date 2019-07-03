#!/usr/bin/python
#
# Naturebytes Wildlife Cam Kit | V1.07 (Pixel)
# Based on the excellent official Raspberry Pi tutorials and a little extra from Naturebytes
#
# Usage sudo python nbphoto_timelapse.py [<options>] [--]
# ======================================================================

from time import sleep
from picamera import PiCamera
import getopt
import sys
import logging
import RPi.GPIO as GPIO
from subprocess import call
from datetime import datetime

# Logging all of the camera's activity to the "naturebytes_camera_log" file. If you want to watch what your camera
# is doing step by step you can open a Terminal window and type "cd /Naturebytes/Scripts" and then type
# "tail -f naturebytes_camera_log" - leave this Terminal window open and you can view the logs live
# Alternatively, add -v to the launch to use verbosity mode

logging.basicConfig(format="%(asctime)s %(message)s",filename="naturebytes_camera_log",level=logging.DEBUG)
logging.info("Naturebytes Wildlife Cam Kit started up successfully")

def main(argv):    
    # Set default save location
    save_location = "/media/usb0/"
    # Set default sleep time 
    sleep_time = 120
    # Command line defaults
    verbose = False

    # Set save location
    try:
        opts, args = getopt.getopt(argv, "hot:v")
        for opt, arg in opts:
            if opt == "-h":
                printHelp()
                sys.exit()
            elif opt == "-o": # Basic error checking
                save_location = arg.strip()
                save_location = save_location if save_location.startswith("/") else "/" + save_location
                save_location = save_location if save_location.endswith("/") else save_location + "/"
            elif opt == "-t":
                sleep_time = int(arg)
    except getopt.GetoptError as err:
        print(str(err))
        printHelp()
        sys.exit(2)

    logging.info("Time lapse started with %i second delay" % sleep_time)

    # Take time lapse image series
    try:

        # for filename in camera.capture_continuous(save_location + "img{counter:03d}_{timestamp:%Y-%m-%d-%H-%M}.jpg"):
        #     print("Captured %s" % filename)
        while True:
            i = datetime.now() # Get current time
            get_date = i.strftime("%Y-%m-%d") # Get and format the date
            get_time = i.strftime("%H-%M-%S.%f") # Get and format the time

            logging.info("Time lapse photo taken")
            printVerbose(verbose, "Time lapse photo taken")

            # Assigning a variable so we can create an image file that contains the date and time as its name
            photo_name = get_date + "_" +  get_time + ".png"

            # Using the raspistill library to take a photo. 
            # cmd = "raspistill -t 300 -w 1920 -h 1440 --nopreview -o " + save_location + photo_name

            # Using the pylepton 
            cmd = "pylepton_capture " + save_location + photo_name

            call ([cmd], shell=True)

            sleep(sleep_time)
    except KeyboardInterrupt:
        print("KeyboardInterrupt detected. Exiting program")
        sys.exit()
    except Exception as e:
        print(e)
        print("Error detected. Exiting program")
        sys.exit(2)

def printHelp():
    options = """
            usage: sudo python nbcamera_timelapse.py [<options>] [--]
            Options: 
            \t -o <outputlocation> \t specify output file location
            \t -t <sleepTime> \t specify sleep time
            """
    print(options)

def printVerbose(verbose, msg):
    if(verbose): print("Log: " + msg)

if __name__ == "__main__":
    main(sys.argv[1:])
