#!/usr/bin/env python

# Quick data recording script for the ADXL345

import time
import Adafruit_ADXL345

#Configure ADXL345
accel = Adafruit_ADXL345.ADXL345()
accel.set_data_rate(Adafruit_ADXL345.ADXL345_DATARATE_100_HZ)

time = time.ctime()
time = time.replace(" ","_")
time = time.replace(":","-")

file_name = "/home/pi/Documents/minion_data/%s_ACC.txt" % time

file = open(file_name,"w+")

file.write("%s\r\n" % time)
file.write("X,Y,Z = +/- 2g\r\n")

print time

while True:
    # Read the X, Y, Z axis acceleration values and print them.
	x, y, z = accel.read()
	file.write('{0},{1},{2}\n'.format(x, y, z))

