import picar_4wd as fc
import sys
import tty
import termios
from threading import *
import time

power_val = 50
key = 'status'
distance_covered = 0.0
speed_cum = 0.0
speed_num = 0
avg_speed = 0.0
running = 1

def speedometer_handler():
    global speed_num
    global speed_cum
    global avg_speed
    global distance_covered
    global running

    while running:
        current_speed = fc.speed_val()
        distance_covered += current_speed * 0.5
        print("Distance Covered: {}".format(distance_covered))
        speed_num += 1
        speed_cum += current_speed
        avg_speed = round(speed_cum/speed_num, 2)
        print("Average Speed: {}".format(avg_speed))
        time.sleep(0.5)

def fire_up_thread():
    speedometer = Thread(target=speedometer_handler)
    speedometer.start()

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
    while True:
        global power_val
        key=readkey()
        if key=='6':
            if power_val <=90:
                power_val += 10
                print("power_val:",power_val)
        elif key=='4':
            if power_val >=10:
                power_val -= 10
                print("power_val:",power_val)

        if key=='w':
            fc.forward(power_val)
        elif key=='a':
            fc.turn_left(power_val)
        elif key=='s':
            fc.backward(power_val)
        elif key=='d':
            fc.turn_right(power_val)
        elif key=='n':
            turn_servo(0)
        elif key=='m':
            turn_servo(1)
        else:
            fc.stop()
        if key=='q':
            print("quit")  
            break  

if __name__ == '__main__':
    fc.start_speed_thread()
    fire_up_thread()
    Keyborad_control()
    running = 0
