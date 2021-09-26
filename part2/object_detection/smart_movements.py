import sys

import signal
import threading

import picar_4wd as fc
import detect_picamera as detect

from time import sleep

vision = detect.Vision()
stopSignDetected = threading.Event()

def kill_program(sig, frame):
    print("Killing smart movement")
    del vision
    sys.exit(0)

signal.signal(signal.SIGINT, kill_program)

def movement():
    global stopSignDetected
    while True:
        if(stopSignDetected.is_set()):
            print("reacting to stopsign")
            fc.turn_left(90)
            sleep(1)
            fc.forward(0)
            sleep(3)
            stopSignDetected.clear()
        else: 
            fc.forward(20)
            sleep(1)

def vision():
    while (True):
        if (vision.scanStopSign()):
            print("thread detect stopsign")
            stopSignDetected.set()
            sleep(10)
        

def main():
    stopSignDetected.clear()
    fc.servo.set_angle(0)

    visionThread = threading.Thread(target=vision)
    # vision & ultrasonic are daemon threads (dependent on movement)
    visionThread.daemon = True

    # start all the threads
    visionThread.start()

    movement()




if __name__ == '__main__':
      main()

