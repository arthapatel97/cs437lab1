import sys

import signal
import threading

import picar_4wd as fc
import detect_picamera as detect

from time import sleep

stopSignDetected = False

def kill_program(sig, frame):
    print("Killing smart movement")
    sys.exit(0)

signal.signal(signal.SIGINT, kill_program)

def movement():
    global stopSignDetected
    while True:
        if(stopSignDetected):
            print("reacting to stopsign")
            fc.turn_left(90)
            sleep(1)
            fc.forward(0)
            sleep(3)
            stopSignDetected = False
        else: 
            fc.forward(20)
            sleep(1)

def vision():
    global stopSignDetected
    while (True):
        if (detect.scanStopSign()):
            print("thread detect stopsign")
            stopSignDetected = True
            sleep(10)
        

def main():
    visionThread = threading.Thread(target=vision)
    fc.servo.set_angle(0)

    # vision & ultrasonic are daemon threads (dependent on movement)
    visionThread.daemon = True

    # start all the threads
    visionThread.start()

    movement()




if __name__ == '__main__':
      main()

