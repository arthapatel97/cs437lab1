import picar_4wd as fc
import sys
import tty
import termios
from threading import *
import time
import signal
from part2.position_tracker.PositionMessage import *
from part2.position_tracker.PositionLogger import *
from part2.environmentMapping.environmentGrid import *
from part2.environmentMapping.uv_scan import *

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
keyboard_thread: Thread = None
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
    while running:
        key=readkey()
        print(key)

print("If you want the program quit. Please press q")
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
    print("Current Angle: {}".format(fc.current_angle))
    print("Current Reading on Sensor: {}".format(fc.us.get_distance()))

def Keyborad_control():
    global power_val
    global running
    global orientation_degree
    global current_position
    global avg_speed

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
        elif key=='a':
            message = PositionMessage(orientation_degree, current_position, avg_speed, TURNING_LEFT)
            logger.append_log(message)
            fc.turn_left(power_val)
        elif key=='s':
            message = PositionMessage(orientation_degree, current_position, avg_speed, MOVING_FORWARD)
            logger.append_log(message)
            fc.backward(power_val)
        elif key=='d':
            message = PositionMessage(orientation_degree, current_position, avg_speed, TURNING_RIGHT)
            logger.append_log(message)
            fc.turn_right(power_val)
        elif key=='n':
            turn_servo(0)
        elif key=='m':
            turn_servo(1)
        else:
            message = PositionMessage(orientation_degree, current_position, avg_speed, IDLE)
            logger.append_log(message)
            fc.stop() 
        key = 'status'

def start_speedometer_thread():
    global speedometer_thread
    speedometer_thread = Thread(target=speedometer_handler)
    speedometer_thread.start()

def start_keyboard_thread():
    global keyboard_thread
    keyboard_thread = Thread(target=Keyborad_control)
    keyboard_thread.start()

def start_key_thread():
    global key_thread
    key_thread = Thread(target=Keyborad_control)
    key_thread.start()

def start_key_thread():
    global key_thread
    key_thread = Thread(target=key_reader_handler)
    key_thread.start()

def fire_up_threads():
    # fc.start_speed_thread()
    # start_speedometer_thread()
    # start_keyboard_thread()
    start_key_thread()

def signal_handler(sig, frame):
    global running
    global distance_covered 
    global avg_speed
    running = 0
    print("Distance Covered: {}".format(distance_covered))
    print("Average Speed: {}".format(avg_speed))
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
    map = EnvironmentGrid()
    current_position = map.getCurrentPosition()
    orientation_degree = 0
    logger = PositionLogger()
    start_message = PositionMessage(orientation_degree, current_position, 0, IDLE)
    logger.append_log(start_message)
    fire_up_threads()
