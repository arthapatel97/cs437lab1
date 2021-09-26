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

    while running:
        current_speed = fc.speed_val()
        distance_covered += current_speed * 0.5
        # print("Distance Covered: {}".format(distance_covered))
        speed_num += 1
        speed_cum += current_speed
        avg_speed = round(speed_cum/speed_num, 2)
        # print("Average Speed: {}".format(avg_speed))
        time.sleep(0.5)

def key_reader_handler():
    global key
    global running

    while running:
        print("reading key")
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
    # print("Current Angle: {}".format(fc.current_angle))
    # print("Current Reading on Sensor: {}".format(fc.us.get_distance()))

def driver_control():
    global power_val
    global running
    global orientation_degree
    global current_position
    global avg_speed
    global key
    print("this is the driver thread...")
    while running:
        if key=='6':
            if power_val <=90:
                power_val += 10
                print("power_val:",power_val)
        elif key=='4':
            if power_val >=10:
                power_val -= 10
                print("power_val:",power_val)
        if key=='w':
            message = PositionMessage(orientation_degree, current_position, avg_speed, MOVING_FORWARD)
            logger.append_log(message)
            fc.forward(power_val)
            time.sleep(0.1)
        elif key=='a':
            message = PositionMessage(orientation_degree, current_position, avg_speed, TURNING_LEFT)
            logger.append_log(message)
            fc.turn_left(power_val)
            time.sleep(0.1)
        elif key=='s':
            message = PositionMessage(orientation_degree, current_position, avg_speed, MOVING_FORWARD)
            logger.append_log(message)
            fc.backward(power_val)
            time.sleep(0.1)
        elif key=='d':
            message = PositionMessage(orientation_degree, current_position, avg_speed, TURNING_RIGHT)
            logger.append_log(message)
            fc.turn_right(power_val)
            time.sleep(0.1)
        elif key=='n':
            turn_servo(0)
            time.sleep(0.1)
        elif key=='m':
            turn_servo(1)
            time.sleep(0.1)
        elif key=='o':
            fc.stop()
        else:
            message = PositionMessage(orientation_degree, current_position, avg_speed, IDLE)
            logger.append_log(message)
            fc.stop() 
            # key = 'status'

def start_speedometer_thread():
    global speedometer_thread
    speedometer_thread = Thread(target=speedometer_handler)
    speedometer_thread.start()

# def start_driver_thread():
#     global driver_thread
#     driver_thread = Thread(target=driver_control)
#     driver_thread.start()

def start_key_thread():
    global key_thread
    key_thread = Thread(target=key_reader_handler)
    key_thread.start()

def fire_up_threads():
    # fc.start_speed_thread()
    # start_speedometer_thread()
    start_key_thread()

# def signal_handler(sig, frame):
#     global running
#     global distance_covered 
#     global avg_speed
#     print("singnal caught")
#     running = 0
#     # print("Distance Covered: {}".format(distance_covered))
#     # print("Average Speed: {}".format(avg_speed))
#     sys.exit(0)

# signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
    logger = PositionLogger()
    map = EnvironmentGrid()
    current_position = map.getCurrentPosition(logger=logger)
    orientation_degree = 0
    start_message = PositionMessage(orientation_degree, current_position, 0, IDLE)
    logger.append_log(start_message)
    print("program has started... Ctrl+C to end")
    fire_up_threads()
    driver_control()
    fc.stop()
