
import time

class radar_new():
    def __init__(self, raspGPIO):
        self.TRIGGER01 = 19
        self.ECHO01 = 26

        self.TRIGGER02 = 13
        self.ECHO02 = 6

        self.TRIGGER03 = 5
        self.ECHO03 = 11

        self.TRIGGER04 = 9
        self.ECHO04 = 10
        self.raspGPIO = raspGPIO

    def initialize(self):
        #set self.raspGPIO directions (in/out
        self.raspGPIO.setup(self.TRIGGER01, self.raspGPIO.OUT)
        self.raspGPIO.setup(self.ECHO01, self.raspGPIO.IN)

        self.raspGPIO.setup(self.TRIGGER02, self.raspGPIO.OUT)
        self.raspGPIO.setup(self.ECHO02, self.raspGPIO.IN)

        self.raspGPIO.setup(self.TRIGGER03, self.raspGPIO.OUT)
        self.raspGPIO.setup(self.ECHO03, self.raspGPIO.IN)

        self.raspGPIO.setup(self.TRIGGER04, self.raspGPIO.OUT)
        self.raspGPIO.setup(self.ECHO04, self.raspGPIO.IN)
        
        self.raspGPIO.output(self.TRIGGER01, False)
        self.raspGPIO.output(self.TRIGGER02, False)
        self.raspGPIO.output(self.TRIGGER03, False)
        self.raspGPIO.output(self.TRIGGER04, False)
        time.sleep(2)

    def distance(self, TRIGGER, ECHO):
        self.raspGPIO.output(TRIGGER, True)
        time.sleep(0.00001)
        self.raspGPIO.output(TRIGGER, False)

        startTime = time.time()
        stopTime = time.time()

        while self.raspGPIO.input(ECHO) == 0:
            startTime = time.time()

        while self.raspGPIO.input(ECHO) == 1:
            stopTime = time.time()
        
        timeElapsed = stopTime - startTime
        distance = (timeElapsed * 34300)/2
        return int(distance)

    def test(self):
        if len(self.get_distancias()) > 0:
            return "RADAR OK"
        return "RADAR FAIL"

    def get_distancias(self):
        distancias = []
        distancias.append(self.distance(self.TRIGGER01, self.ECHO01))
        distancias.append(self.distance(self.TRIGGER02, self.ECHO02))
        distancias.append(self.distance(self.TRIGGER03, self.ECHO03))
        distancias.append(self.distance(self.TRIGGER04, self.ECHO04))
        time.sleep(1)
        return distancias

if __name__ == "__main__":
    
    radar 