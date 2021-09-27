import sys

import signal
import threading

import picar_4wd as fc
import detect_picamera as detect

from time import sleep

visionObject = detect.Vision()
stopSignDetected = threading.Event()
stopSignCleared = threading.Event()

def kill_program(sig, frame):
    global visionObject
    print("Killing smart movement")
    del visionObject

    fc.forward(0)
    sys.exit(0)

signal.signal(signal.SIGINT, kill_program)

def movement():
    while True:
        if(stopSignDetected.is_set()):
            stopSignMove()

            # greenlight to vision
            stopSignDetected.clear()
            stopSignCleared.set()
        else: 
            fc.forward(20)
            sleep(.001)

def stopSignMove():
    print("reacting to stopsign")
    # Stops for .5s
    fc.forward(0)
    sleep(0.5)

    # Squiggle for some time
    for i in range(2):
        fc.backward(10)
        sleep(0.2)
        fc.forward(10)
        sleep(0.2)

    # Stops for 2s
    fc.forward(0)
    sleep(2)

    # Turns left
    fc.turn_left(90)
    sleep(0.8)

def vision():
    while (True):
        if (visionObject.scanStopSign()):
            print("thread detect stopsign")
            stopSignDetected.set()

            # wait until avoidance sequence is done
            stopSignCleared.wait()
            stopSignCleared.clear()
        

def main():
    stopSignDetected.clear()
    stopSignCleared.clear()
    fc.servo.set_angle(0)

    visionThread = threading.Thread(target=vision)
    # vision & ultrasonic are daemon threads (dependent on movement)
    visionThread.daemon = True

    # start all the threads
    visionThread.start()

    movement()

if __name__ == '__main__':
      main()

