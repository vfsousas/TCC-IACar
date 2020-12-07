
import RPi.GPIO as GPIO
import time
import board
import board, busio, adafruit_vl53l0x


i2c = busio.I2C(board.SCL, board.SDA)
VL53 = adafruit_vl53l0x.VL53L0X(i2c)

xhut = [
    
]

print(VL53.range)
