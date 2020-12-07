
import RPi.GPIO as GPIO
import time
import board
import board, busio, adafruit_vl53l0x
from digitalio import DigitalInOut

import VL53L0X

objGPIO = GPIO
objGPIO.cleanup() # limpa todos os estados de todas as portasmotorCar.
objGPIO.setmode(GPIO.BCM) #Definindi uso dos numeros das portas por canais

xhut1 = 4 
xhut2 = 17
xhut3 = 27

objGPIO.setup(xhut1, GPIO.OUT)
objGPIO.setup(xhut1, GPIO.LOW)

objGPIO.setup(xhut2, GPIO.OUT)
objGPIO.setup(xhut2, GPIO.LOW)

objGPIO.setup(xhut3, GPIO.OUT)
objGPIO.setup(xhut3, GPIO.LOW)


time.sleep(1)


objGPIO.setup(xhut1, GPIO.HIGH)
time.sleep(1)
tof = VL53L0X.VL53L0X(i2c_address=0x29)
##tof.change_address(new_address=0x2D)#
tof.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BEST)
tof.get_distance()

#objGPIO.setup(xhut2, GPIO.HIGH)
#time.sleep(1)
#tof2 = VL53L0X.VL53L0X(i2c_bus=1, i2c_address=0x29)
#tof2.change_address(new_address=0x2B)        


#objGPIO.setup(xhut3, GPIO.HIGH)
#time.sleep(1)
#tof3 = VL53L0X.VL53L0X(i2c_bus=1, i2c_address=0x2D)
#tof3.change_address(new_address=0x2F)        
#tof3.start_ranging()

#time.sleep(2)
#tof.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)


#timing = tof.get_timing()

