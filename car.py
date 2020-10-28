import RPi.raspGPIO as raspGPIO
import time

move = 5
self.raspGPIO.setwarnings(False) 
self.raspGPIO.setmode(self.raspGPIO.BOARD)
#Rodas dianteiras
RDEF = 38
RDDF = 29
RDER = 40
RDDR = 13

RTEF = 32
RTDF = 15
RTER = 36
RTDR = 11
self.self.raspGPIO.setup(RDEF, self.raspGPIO.OUT)
self.self.raspGPIO.setup(RDDF, self.raspGPIO.OUT)
self.self.raspGPIO.setup(RDER, self.raspGPIO.OUT)
self.self.raspGPIO.setup(RDDR, self.raspGPIO.OUT)
self.self.raspGPIO.setup(RTEF, self.raspGPIO.OUT)
self.self.raspGPIO.setup(RTDF, self.raspGPIO.OUT)
self.self.raspGPIO.setup(RTER, self.raspGPIO.OUT)
self.self.raspGPIO.setup(RTDR, self.raspGPIO.OUT)

def stop():
    self.raspGPIO.output(self.RDEF, self.raspGPIO.LOW)
    self.raspGPIO.output(self.RDDF, self.raspGPIO.LOW)
    self.raspGPIO.output(self.RDER, self.raspGPIO.LOW)
    self.raspGPIO.output(self.RDDR, self.raspGPIO.LOW)
    self.raspGPIO.output(self.RTEF, self.raspGPIO.LOW)
    self.raspGPIO.output(self.RTDF, self.raspGPIO.LOW)
    self.raspGPIO.output(self.RTER, self.raspGPIO.LOW)
    self.raspGPIO.output(self.RTDR, self.raspGPIO.LOW)

def forward():
    self.raspGPIO.output(self.RDEF, self.raspGPIO.HIGH)
    self.raspGPIO.output(self.RDDF, self.raspGPIO.HIGH)
    self.raspGPIO.output(self.RTEF, self.raspGPIO.HIGH)
    self.raspGPIO.output(self.RTDF, self.raspGPIO.HIGH)


def backward():
    self.raspGPIO.output(self.RDER, self.raspGPIO.HIGH)
    self.raspGPIO.output(self.RDDR, self.raspGPIO.HIGH)
    self.raspGPIO.output(self.RTER, self.raspGPIO.HIGH)
    self.raspGPIO.output(self.RTDR, self.raspGPIO.HIGH)
    
def left_forward():
    self.raspGPIO.output(self.RDEF, self.raspGPIO.HIGH)
    self.raspGPIO.output(self.RTEF, self.raspGPIO.HIGH)


def RIGHT_forward():
    self.raspGPIO.output(self.RDDF, self.raspGPIO.HIGH)
    self.raspGPIO.output(self.RTDF, self.raspGPIO.HIGH)

def setMov(value):
    global move
    move=value

def changeMove(move):
    print("Neew Move",move)
    if(move==5):
        print("Stop")
        stop()

    if(move==0):
        print("Frente")
        forward()

    if(move==1):
        left_forward()

    if(move==2):
        RIGHT_forward()

    if(move==3):
        backward()
    time.sleep(1)

if __name__ == "__main__":
    stop()
    forward()
    time.sleep(3)
    stop()
    backward()
    time.sleep(3)
    stop()
    left_forward()
    time.sleep(3)
    stop()
    RIGHT_forward()
    time.sleep(3)
    stop()
    
    self.raspGPIO.cleanup()



class MotorCarro:
    def __init__(self, raspGPIO):
        #GPIO Rodas dianteiras
        self.RDEF = 38
        self.RDDF = 29
        self.RDER = 40
        self.RDDR = 13

        #GPIO Rodas dianteiras
        self.RTEF = 32
        self.RTDF = 15
        self.RTER = 36
        self.RTDR = 11
        self.raspGPIO = raspGPIO
        self.raspGPIO.setup(self.RDEF, self.raspGPIO.OUT)
        self.raspGPIO.setup(self.RDDF, self.raspGPIO.OUT)
        self.raspGPIO.setup(self.RDER, self.raspGPIO.OUT)
        self.raspGPIO.setup(self.RDDR, self.raspGPIO.OUT)
        self.raspGPIO.setup(self.RTEF, self.raspGPIO.OUT)
        self.raspGPIO.setup(self.RTDF, self.raspGPIO.OUT)
        self.raspGPIO.setup(self.RTER, self.raspGPIO.OUT)
        self.raspGPIO.setup(self.RTDR, self.raspGPIO.OUT)

        def stop(self):
            self.raspGPIO.output(self.RDEF, self.raspGPIO.LOW)
            self.raspGPIO.output(self.RDDF, self.raspGPIO.LOW)
            self.raspGPIO.output(self.RDER, self.raspGPIO.LOW)
            self.raspGPIO.output(self.RDDR, self.raspGPIO.LOW)
            self.raspGPIO.output(self.RTEF, self.raspGPIO.LOW)
            self.raspGPIO.output(self.RTDF, self.raspGPIO.LOW)
            self.raspGPIO.output(self.RTER, self.raspGPIO.LOW)
            self.raspGPIO.output(self.RTDR, self.raspGPIO.LOW)

        def forward():
            self.raspGPIO.output(self.RDEF, self.raspGPIO.HIGH)
            self.raspGPIO.output(self.RDDF, self.raspGPIO.HIGH)
            self.raspGPIO.output(self.RTEF, self.raspGPIO.HIGH)
            self.raspGPIO.output(self.RTDF, self.raspGPIO.HIGH)
        

        def backward():
            self.raspGPIO.output(self.RDER, self.raspGPIO.HIGH)
            self.raspGPIO.output(self.RDDR, self.raspGPIO.HIGH)
            self.raspGPIO.output(self.RTER, self.raspGPIO.HIGH)
            self.raspGPIO.output(self.RTDR, self.raspGPIO.HIGH)
            
        def left_forward():
            self.raspGPIO.output(self.RDEF, self.raspGPIO.HIGH)
            self.raspGPIO.output(self.RTEF, self.raspGPIO.HIGH)


        def right_forward():
            self.raspGPIO.output(self.RDDF, self.raspGPIO.HIGH)
            self.raspGPIO.output(self.RTDF, self.raspGPIO.HIGH)

        def left_backward():
            self.raspGPIO.output(self.RDER, self.raspGPIO.HIGH)
            self.raspGPIO.output(self.RTER, self.raspGPIO.HIGH)

        def right_backward():
            self.raspGPIO.output(self.RDDR, self.raspGPIO.HIGH)
            self.raspGPIO.output(self.RTDR, self.raspGPIO.HIGH)
        
        def movimentacarro(self, movimento):
            if movimento==0:
                self.forward()
            elif movimento==1:
                self.backward()
            elif movimento=2:
                self.left_forward()
            elif movimento==3:
                self.right_forward()
            elif movimento==4:
                self.left_backward()
            elif movimento==5:
                self.right_backward()
  
            time.sleep(5)
            self.stop()

