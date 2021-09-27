import picar_4wd as fc
import sys
import tty
import termios
from threading import *
import time
import signal
from PositionMessage import *
from PositionLogger import *
from environmentGrid import *
from uv_scan import *

power_val = 50
key = 'status'
distance_covered = 0.0
speed_cum = 0.0
speed_num = 0
avg_speed = 0.0
running = 1
orientation_degree = 0
current_position = (0, 0)

map: EnvironmentGrid = None
logger: PositionLogger = None
speedometer_thread: Thread = None
driver_thread: Thread = None
key_thread: Thread = None

def speedometer_handler():
    global speed_num
    global speed_cum
    global avg_speed
    global distance_covered
    global running
    start = time.monotonic()
    while running:
        current_speed = fc.speed_val()
        speed_num += 1
        speed_cum += current_speed
        avg_speed = round(speed_cum/speed_num, 2)
        time.sleep(0.5)
    diff = (time.monotonic() - start)
    distance_covered = diff * avg_speed

def key_reader_handler():
    global key
    global running

    while running:
        key=readkey()
        print(f"key is {key}")
        if key=='o':
            running = 0

def readchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def readkey(getchar_fn=None):
    getchar = getchar_fn or readchar
    c1 = getchar()
    if ord(c1) != 0x1b:
        return c1
    c2 = getchar()
    if ord(c2) != 0x5b:
        return c1
    c3 = getchar()
    return chr(0x10 + ord(c3) - 65)

def turn_servo(dir: int, at=2):
    if dir == 0:
        if not fc.current_angle >= fc.max_angle:
            fc.current_angle += at
    else:
        if not fc.current_angle <= fc.min_angle:
            fc.current_angle -= at
    fc.servo.set_angle(fc.current_angle)

def driver_control():
    global power_val
    global running
    global orientation_degree
    global current_position
    global avg_speed
    global key
    global map
    global logger

    while running:
        if key=='6':
            if power_val <=90:
                power_val += 10
                print("increased power supply to: {power_val}")
        elif key=='4':
            if power_val >=10:
                power_val -= 10
                print("decreased power supply to: {power_val}")
        if key=='w':
            current_position = map.updateCurrentPositionOrientation(logger)
            logger.append_log(PositionMessage(orientation_degree, current_position, avg_speed, MOVING_FORWARD))
            fc.forward(power_val)
        elif key=='a':
            current_position = map.updateCurrentPositionOrientation(logger)
            logger.append_log(PositionMessage(orientation_degree, current_position, avg_speed, TURNING_LEFT))
            fc.turn_left(power_val)
        elif key=='s':
            current_position = map.updateCurrentPositionOrientation(logger)
            logger.append_log(PositionMessage(orientation_degree, current_position, avg_speed, MOVING_FORWARD))
            fc.backward(power_val)
        elif key=='d':
            current_position = map.updateCurrentPositionOrientation(logger)
            logger.append_log(PositionMessage(orientation_degree, current_position, avg_speed, TURNING_RIGHT))
            fc.turn_right(power_val)
        elif key=='n':
            turn_servo(0)
        elif key=='m':
            turn_servo(1)
        else:
            current_position = map.updateCurrentPositionOrientation(logger)
            logger.append_log(PositionMessage(orientation_degree, current_position, avg_speed, IDLE))
            fc.stop()

def start_speedometer_thread():
    global speedometer_thread
    speedometer_thread = Thread(target=speedometer_handler)
    speedometer_thread.start()

def start_key_thread():
    global key_thread
    key_thread = Thread(target=key_reader_handler)
    key_thread.start()

def fire_up_threads():
    init()
    fc.start_speed_thread()
    start_speedometer_thread()
    start_key_thread()
    driver_control()

def init():
    global logger
    global map
    global current_position
    global orientation_degree

    logger = PositionLogger()
    map = EnvironmentGrid()
    current_position = map.getCurrentPosition(logger=logger)
    orientation_degree = 0
    start_message = PositionMessage(orientation_degree, current_position, 0, IDLE)
    logger.append_log(start_message)

if __name__ == '__main__':
    print("program has started... Ctrl+C to end")
    fire_up_threads()
    fc.stop()
    print("Distance Covered: {}".format(distance_covered))
    print("Average Speed: {}".format(avg_speed))
