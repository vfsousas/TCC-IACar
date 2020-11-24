import VL53L0X
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

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

GPIO.output(XSHUT2, GPIO.HIGH)

tof = VL53L0X.VL53L0X(i2c_bus=0, address=0x2B)
GPIO.setup(XSHUT, GPIO.IN)
tof1 = VL53L0X.VL53L0X(ic2_bus=0)

tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
distance = tof.get_distance()
tof.stop_ranging()
print(distance)

tof1.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
distance = tof1.get_distance()
tof1.stop_ranging()
print(distance)



GPIO.cleanup()
