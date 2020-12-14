
import time
import RPi.GPIO as GPIO
import numpy as np
import math

class driverGPIO():
    def __init__(self):
        self.GPIO = GPIO
        self.GPIO.cleanup()
        self.GPIO.setmode(GPIO.BCM)

    
    def getGPIO(self):
        return self.GPIO

class radar_new():
    def __init__(self, raspGPIO, motor, servor):
        self.arrtrgEcho = [[26,19], [6,13], [23,24], [25,9]]
        self.motorCarro = motor
        self.servo = servor
        #self.TRIGGER01 = 19
        #self.ECHO01 = 26

        #self.TRIGGER02 = 13
        #self.ECHO02 = 6

        #self.TRIGGER03 = 5
        #self.ECHO03 = 11

        #self.TRIGGER04 = 10
        #self.ECHO04 = 9
        self.raspGPIO = raspGPIO

    def initialize(self):
        #set self.raspGPIO directions (in/out
        for i in range(len(self.arrtrgEcho)):
            self.raspGPIO.setup(self.arrtrgEcho[i][0], self.raspGPIO.OUT)
            self.raspGPIO.setup(self.arrtrgEcho[i][1], self.raspGPIO.IN)

        #self.raspGPIO.setup(self.TRIGGER02, self.raspGPIO.OUT)
        #self.raspGPIO.setup(self.ECHO02, self.raspGPIO.IN)

        #self.raspGPIO.setup(self.TRIGGER03, self.raspGPIO.OUT)
        #self.raspGPIO.setup(self.ECHO03, self.raspGPIO.IN)

        #self.raspGPIO.setup(self.TRIGGER04, self.raspGPIO.OUT)
        #self.raspGPIO.setup(self.ECHO04, self.raspGPIO.IN)
        
        #self.raspGPIO.output(self.TRIGGER01, False)
        #self.raspGPIO.output(self.TRIGGER02, False)
        #self.raspGPIO.output(self.TRIGGER03, False)
        #self.raspGPIO.output(self.TRIGGER04, False)
        time.sleep(2)
    
    def distance2(self, pointer):
        print(self.arrtrgEcho[pointer][0])
        self.raspGPIO.setup(self.arrtrgEcho[i][0], self.raspGPIO.OUT)
        self.raspGPIO.setup(self.arrtrgEcho[i][1], self.raspGPIO.IN)
        self.raspGPIO.output(self.arrtrgEcho[pointer][0], True)
        time.sleep(2)
        self.raspGPIO.output(self.arrtrgEcho[pointer][0], False)


    def distance(self, pointer):
        self.raspGPIO.setup(self.arrtrgEcho[pointer][0], self.raspGPIO.OUT)
        self.raspGPIO.setup(self.arrtrgEcho[pointer][1], self.raspGPIO.IN)
        self.raspGPIO.output(self.arrtrgEcho[pointer][0], True)
        time.sleep(0.00001)
        self.raspGPIO.output(self.arrtrgEcho[pointer][0], False)
        counter =0
        new_reading = False
        startTime = time.time()
        stopTime = time.time()
            
        while self.raspGPIO.input(self.arrtrgEcho[pointer][1]) == 0:
            startTime = time.time()
            counter += 1
            if counter == 5000:
                self.raspGPIO.cleanup()
                self.raspGPIO.setmode(GPIO.BCM)
                self.motorCarro.activateweels()
                self.servo.activateservo()
                return -1

        while self.raspGPIO.input(self.arrtrgEcho[pointer][1]) == 1:
            stopTime = time.time()
      
       
        
        timeElapsed = stopTime - startTime
        distance = (timeElapsed * 34300)/2
        if distance > 189:
            return -1
        if math.isnan(distance):
            return -1

        return int(distance)

    def test(self):
        if len(self.get_distancias()) > 0:
            return "RADAR OK"
        return "RADAR FAIL"

    def get_distancias(self):
        distancias = []
        for i in range(4):
            dist = self.distance(i)
            while dist == -1:
                dist = self.distance(i)

            distancias.append(dist)
        return distancias

if __name__ == "__main__":
    driverG = driverGPIO()
    radar = radar_new(driverG.getGPIO())
    radar.initialize()
    count=0
    while count<3000:
        print(radar.get_distancias())
        count+=1