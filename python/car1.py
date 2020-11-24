#!/usr/bin/python

# MIT License
# 
# Copyright (c) 2017 John Bryan Moore
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import time
import VL53L0X
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BOARD)

GPIO_trigger7 = 7
GPIO_trigger11 = 11
GPIO_trigger13 = 13
GPIO_trigger15 = 15

GPIO.setup(GPIO_trigger7, GPIO.OUT)
GPIO.setup(GPIO_trigger11, GPIO.OUT)
GPIO.setup(GPIO_trigger13, GPIO.OUT)
GPIO.setup(GPIO_trigger15, GPIO.OUT)

GPIO_trigger31= 31
GPIO_trigger33 = 33
GPIO_trigger35 = 35
GPIO_trigger37 = 37

GPIO.setup(GPIO_trigger31, GPIO.OUT)
GPIO.setup(GPIO_trigger33, GPIO.OUT)
GPIO.setup(GPIO_trigger35, GPIO.OUT)
GPIO.setup(GPIO_trigger37, GPIO.OUT)

XSHUT=12
XSHUT2=29

# Setup GPIO for shutdown pins on each VL53L0X
GPIO.setup(XSHUT, GPIO.OUT)
GPIO.setup(XSHUT2, GPIO.OUT)

# Set all shutdown pins low to turn off each VL53L0X
GPIO.output(XSHUT, GPIO.LOW)
GPIO.output(XSHUT2, GPIO.LOW)

# Keep all low for 500 ms or so to make sure they reset
time.sleep(0.50)

# Create one object per VL53L0X passing the address to give to
# each.
tof = VL53L0X.VL53L0X(i2c_bus=0, address=0x2B)
GPIO.setup(XSHUT, GPIO.IN)
tof1 = VL53L0X.VL53L0X(ic2_bus=0, address=0x2d)
#GPIO.setup(XSHUT2, GPIO.IN)

time.sleep(0.50)
#tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

# Set shutdown pin high for the second VL53L0X then 
# call to start ranging 

timing = tof.get_timing()
if (timing < 20000):
    timing = 20000
print ("Timing %d ms" % (timing/1000))

for count in range(1,10):
    #tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
    distance = tof.get_distance()
    #tof.stop_ranging()

    if (distance > 0):
        print ("sensor %d - %d mm, %d cm, iteration %d" % (tof.my_object_number, distance, (distance/10), count))
    else:
        print ("%d - Error tof" % tof.my_object_number)

    #tof1.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
    distance = tof1.get_distance()
    #tof1.stop_ranging()

    if (distance > 0):
        print ("sensor %d - %d mm, %d cm, iteration %d" % (tof1.my_object_number, distance, (distance/10), count))
    else:
        print ("%d - Error tof1" % tof.my_object_number)

    time.sleep(timing/1000000.00)

if __name__ == "__main__":
    GPIO.output(GPIO_trigger7, False)
    GPIO.output(GPIO_trigger11, False)

    GPIO.output(GPIO_trigger13, False)
    GPIO.output(GPIO_trigger15, False)


    GPIO.output(GPIO_trigger31, False)
    GPIO.output(GPIO_trigger33, False)

    GPIO.output(GPIO_trigger35, False)
    GPIO.output(GPIO_trigger37, False)

  
    GPIO.output(GPIO_trigger11, True)
    GPIO.output(GPIO_trigger13, True)

    GPIO.output(GPIO_trigger33, True)
    GPIO.output(GPIO_trigger35, True)

    time.sleep(5)
    GPIO.output(GPIO_trigger11, False)
    GPIO.output(GPIO_trigger13, False)
    GPIO.output(GPIO_trigger33, False)
    GPIO.output(GPIO_trigger35, False)
    GPIO.cleanup()


