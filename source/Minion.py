#!/usr/bin/env python

from picamera import PiCamera
import RPi.GPIO as GPIO
import time
import os

GPIO.setwarnings(False)

i = 0
light = 12
wifi = 7

ifswitch = "sudo /home/pi/Documents/Minion_tools/dhcp-switch.py"

iwlist = 'sudo iwlist wlan0 scan | grep "Class_Hub"'

net_cfg = "ls /etc/ | grep dhcp"

ping_hub = "ping 192.168.0.1 -c 1"

ping_google = "ping google.com -c 1"

subp = "sudo pkill -9 -f ADXL345_Sampler_100Hz.py"

def flash():
        j = 0
        while j <= 1:
                GPIO.output(light, 1)
                time.sleep(.25)
                GPIO.output(light, 0)
                time.sleep(.25)
                j = j + 1

def off():
	GPIO.output(light, 0)

def on():
	GPIO.output(light, 1)

def picture():

        pictime = os.popen("sudo hwclock -r").read()
        pictime = pictime.split('.',1)[0]
        pictime = pictime.replace("  ","_")
        pictime = pictime.replace(" ","_")
        pictime = pictime.replace(":","-")
	    on()
        camera.resolution = (2592, 1944)
        camera.framerate = 15
        camera.start_preview()
    	time.sleep(10)
    	camera.capture('/home/pi/Documents/minion_pics/%s.jpg' % pictime)
    	time.sleep(5)
    	camera.stop_preview()
    	off()

if __name__ == '__main__':

   	camera = PiCamera()
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(light, GPIO.OUT)
	GPIO.setup(wifi, GPIO.OUT)
	GPIO.output(wifi, 1)
	picture()

        wifi_status = os.popen(iwlist).read()

        if "Class_Hub" in wifi_status:
                print "WIFI!!"
                status = "Connected"
                net_status = os.popen(net_cfg).read()
                if ".minion" in net_status:
                        os.system(ifswitch)
                else:
                        print "You have Minions!"

        else:
		print "No WIFI found."
                status = "Not Connected"

        print status

	if status == "Connected":
		os.system(subp)
		flash()
		quit()
	else:
		print 'Goodbye'
		GPIO.output(wifi, 0)
		time.sleep(3)
		os.system('sudo shutdown now')
