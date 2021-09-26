import picar_4wd as fc
import time
import random
from threading import *
from queue import *

speed = 50
status = 0

q: Queue = None
us_scanning_thread: Thread = None

def us_scanning_handler():
    global status
    global q
    while True:
        status = fc.get_status_at(0)
        
        pass

def driving_handler():
    global status
    global q

    while True:



def main():
    while True:
        scan_list = fc.scan_step(35)
        if not scan_list:
            continue

        tmp = scan_list[3:7]
        print(tmp)
        if tmp != [2,2,2,2]:
            fc.backward(speed)
            time.sleep(0.5)
            turn_direction = random.choice([0,1])
            if (turn_direction):
                fc.turn_right(speed)
            else:
                fc.turn_left(speed)
        else:
            fc.forward(speed)

def start_us_scanning_thread():
    global us_scanning_thread
    us_scanning_thread = Thread(target=)

if __name__ == "__main__":
    try: 
        main()
    finally: 
        fc.stop()
