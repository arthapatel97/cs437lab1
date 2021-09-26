import sys
# sys.path.insert(1, './')

import signal
import threading

import picar_4wd as fc
import part2.object_detection.detect_picamera as detect

from time import sleep

stopSignDetected = threading.Event()

def kill_program(sig, frame):
    print("Killing smart movement")
    sys.exit(0)

signal.signal(signal.SIGINT, kill_program)

def movement():
    while True:
        if(stopSignDetected.is_set):
            fc.turn_left(90)
            sleep(1)
            fc.forward(0)
            sleep(3)

        fc.forward(20)
        sleep(1)

def vision():
    while (True):
        if (detect.scanStopSign()):
            stopSignDetected.set()
            sleep(10)
        

def main():
    visionThread = threading.Thread(target=vision)

    # vision & ultrasonic are daemon threads (dependent on movement)
    visionThread.daemon = True

    # start all the threads
    visionThread.start()

    movement()




if __name__ == '__main__':
      main()

