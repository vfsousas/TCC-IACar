
import time
import RPi.GPIO as GPIO
import numpy as np
import math

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(9, GPIO.IN)
time.sleep(2)

while True:
    GPIO.output(25, True)
    time.sleep(0.00001)
    GPIO.output(25, False)
    startTime = time.time()
    stopTime = time.time()
    counter=0
    while GPIO.input(9) == 0:
        counter += 1
        startTime = time.time()

        if counter == 5000:
            counter=0
            GPIO.cleanup()
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(25, GPIO.OUT)
            GPIO.setup(9, GPIO.IN)
            GPIO.output(25, False)
            print("-1")

    while GPIO.input(9) == 1:
        stopTime = time.time()

    timeElapsed = stopTime - startTime
    distance = (timeElapsed * 34300)/2
    print(distance)