import picar_4wd as fc
import time
import random
from threading import *
from queue import *

TURNING_RIGHT = "TURNING_RIGHT"
TURNING_LEFT = "TURNING_LEFT"
MOVING_FORWARD = "MOVING_FORWARD"
MOVING_BACKWARD = "MOVING_BACKWARD"
IDLE = "IDLE"

speed = 50
status = 0
car_state = IDLE

def driving_handler():
    global status
    global car_state
    global speed

    while True:
        status = fc.get_status_at(0, 50, 20)
        if status == 0:
            fc.stop()
            fc.backward(speed)
            time.sleep(1)
            turn_direction = random.choice([0,1])
            if (turn_direction):
                fc.turn_right(speed)
            else:
                fc.turn_left(speed)
            time.sleep(2)
        elif status == 1:
            speed /= 2
            if car_state == MOVING_FORWARD:
                fc.forward(speed)
            elif car_state == MOVING_FORWARD:
                fc.backward(speed)
        else:
            fc.forward(speed)

if __name__ == "__main__":
    speed = 50
    status = 0
    car_state = IDLE

    try:
        driving_handler
    finally:
        fc.stop()
