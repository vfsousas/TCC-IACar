import RPi.GPIO as GPIO
import time
import board
import board, busio, adafruit_vl53l0x
from digitalio import DigitalInOut



#Setup das portas logicas do Raspibery PI
class SetupGPIO:
    def __init__(self):
        self.objGPIO = GPIO
        #self.objGPIO.cleanup() # limpa todos os estados de todas as portasmotorCar.
        self.objGPIO.setmode(GPIO.BCM) #Definindi uso dos numeros das portas por canais
        self.i2c = None
    
    def get_gpio(self):
        return self.objGPIO

    def clean(self):
        self.objGPIO.cleanup()

    def findSensor(self):
        i2c = board.I2C()
        while not i2c.try_lock():
            pass

        print('I2c', [hex(device_address) for device_address in i2c.scan()])

        i2c.unlock()
    
    def antigo(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        xshut = [ DigitalInOut(board.D13) , DigitalInOut(board.D8) ]

        for power_pin in xshut:
            power_pin.switch_to_output(value=False)

        vl53 = []
        for i, power_pin in enumerate(xshut):
            power_pin.value = True
            vl53.insert(i, adafruit_vl53l0x.VL53L0X(self.i2c))


class Vl53_Radar:
    def __init__(self, raspGPIO):
        #self.i2c = busio.I2C(board.SCL, board.SDA)
        #self.vl53 = adafruit_vl53l0x.VL53L0X(self.i2c)
        import VL53L0X

        self.yarr = []
        self.count = 0
        self.raspGPIO = raspGPIO
        self.raspGPIO.setwarnings(True)

        # GPIO for Sensor 1 shutdown pin
        sensor1_shutdown = 4 
        # GPIO for Sensor 2 shutdown pin
        sensor2_shutdown = 23
        sensor3_shutdown = 24
        self.raspGPIO.setup(sensor1_shutdown, GPIO.OUT)
        self.raspGPIO.setup(sensor2_shutdown, GPIO.OUT)
        self.raspGPIO.setup(sensor3_shutdown, GPIO.OUT)

        # Set all shutdown pins low to turn off each VL53L0X
        self.raspGPIO.output(sensor1_shutdown, GPIO.LOW)
        self.raspGPIO.output(sensor2_shutdown, GPIO.LOW)
        self.raspGPIO.output(sensor3_shutdown, GPIO.LOW)

        self.tof = VL53L0X.VL53L0X(i2c_bus=0, i2c_address=0x29)
        self.tof2 = VL53L0X.VL53L0X(i2c_bus=0, i2c_address=0x2B)
        self.tof3 = VL53L0X.VL53L0X(i2c_bus=0, i2c_address=0x2D)


        self.raspGPIO.output(sensor1_shutdown, GPIO.HIGH)

        time.sleep(0.50)
        try:
            #self.tof3.start_ranging()
            pass
        except Exception as err:
            print(err)
            pass
        #self.tof = VL53L0X.VL53L0X(i2c_address=0x2B)
        #self.tof = VL53L0X.VL53L0X(i2c_address=0x2D)
        # Set shutdown pin high for the first VL53L0X then 
        # call to start ranging 
        time.sleep(0.50)
        #self.tof02 = VL53L0X.VL53L0X(address=0x2a)
        #self.tof03 = VL53L0X.VL53L0X(address=0x2b)

    
    def get_radar(self):
        return self.tof
    
    def get_radar_posicao(self):
        print('self.tof.get_distance()', self.tof.get_distance())
        print('self.tof.get_distance()', self.tof2.get_distance())
        print('self.tof.get_distance()', self.tof3.get_distance())
        return self.tof.get_distance()

    

raspGPIO  = SetupGPIO()
try:
    radar     = Vl53_Radar(raspGPIO.get_gpio())
    raspGPIO.antigo()
    #raspGPIO.findSensor()
except Exception as err:
    print('err', err)
    raspGPIO.clean()
#print(radar.get_radar_posicao())

