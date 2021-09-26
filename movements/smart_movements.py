import signal
import sys
import os

from queue import Queue
import threading
from time import sleep

stopSignDetected = threading.Event()

def kill_program(sig, frame):
    print("Killing smart movement")
    sys.exit(0)

signal.signal(signal.SIGINT, kill_program)

def movement():
    while True:
        print("movement")
        sleep(1)

def vision():
    while (True):
        print("vision")
        sleep(1)

def main():
    visionThread = threading.Thread(target=vision)

    # vision & ultrasonic are daemon threads (dependent on movement)
    visionThread.daemon = True

    # start all the threads
    visionThread.start()

    movement()




if __name__ == '__main__':
      main()

