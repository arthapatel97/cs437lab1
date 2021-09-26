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
    global stopSignDetected
    while True:
        if(stopSignDetected.is_set()):
            print("reacting to stopsign")
            fc.forward(0)
            sleep(3)

            fc.turn_left(40)
            sleep(1.5)

            stopSignDetected.clear()

            # greenlight to vision
            stopSignCleared.set()
        else: 
            fc.forward(20)
            sleep(.001)

def vision():
    while (True):
        if (visionObject.scanStopSign()):
            print("thread detect stopsign")
            stopSignDetected.set()

            # wait until avoidance sequence is done
            stopSignCleared.wait()
            stopSignCleared.clear()
            
            # wait until movement sequence is done
        

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

