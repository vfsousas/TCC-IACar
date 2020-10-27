import RPi.GPIO as GPIO
import time

move = 5
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BOARD)
#Rodas dianteiras
RDEF = 38
RDDF = 29
RDER = 40
RDDR = 13

RTEF = 32
RTDF = 15
RTER = 36
RTDR = 11
GPIO.setup(RDEF, GPIO.OUT)
GPIO.setup(RDDF, GPIO.OUT)
GPIO.setup(RDER, GPIO.OUT)
GPIO.setup(RDDR, GPIO.OUT)
GPIO.setup(RTEF, GPIO.OUT)
GPIO.setup(RTDF, GPIO.OUT)
GPIO.setup(RTER, GPIO.OUT)
GPIO.setup(RTDR, GPIO.OUT)

def stop():
    GPIO.output(RDEF, GPIO.LOW)
    GPIO.output(RDDF, GPIO.LOW)
    GPIO.output(RDER, GPIO.LOW)
    GPIO.output(RDDR, GPIO.LOW)
    GPIO.output(RTEF, GPIO.LOW)
    GPIO.output(RTDF, GPIO.LOW)
    GPIO.output(RTER, GPIO.LOW)
    GPIO.output(RTDR, GPIO.LOW)

def forward():
    GPIO.output(RDEF, GPIO.HIGH)
    GPIO.output(RDDF, GPIO.HIGH)
    GPIO.output(RTEF, GPIO.HIGH)
    GPIO.output(RTDF, GPIO.HIGH)


def backward():
    GPIO.output(RDER, GPIO.HIGH)
    GPIO.output(RDDR, GPIO.HIGH)
    GPIO.output(RTER, GPIO.HIGH)
    GPIO.output(RTDR, GPIO.HIGH)
    
def left_forward():
    GPIO.output(RDEF, GPIO.HIGH)
    GPIO.output(RTEF, GPIO.HIGH)


def RIGHT_forward():
    GPIO.output(RDDF, GPIO.HIGH)
    GPIO.output(RTDF, GPIO.HIGH)

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
    
    GPIO.cleanup()
