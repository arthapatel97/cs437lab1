import picar_4wd as fc
import sys
import tty
import termios
import asyncio
import threading

power_val = 50

servo_step = 2

key = 'status'

distances_list = []
servo_map = []

def init_servo_map(angle_interval=2):
    global servo_map

    angle = fc.max_angle
    while angle >= fc.min_angle:
        angle -= angle_interval
        servo_map.append((angle, 0))


def scan_surrondings(angle_interval=2):
    global servo_map

    fc.servo.set_angle(fc.max_angle)
    while fc.current_angle >= fc.min_angle:
        fc.current_angle -= angle_interval
        fc.servo.set_angle(fc.current_angle)
        servo_map.append((fc.current_angle, fc.us.get_distance()))

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
    scan_surrondings()
    fc.servo.set_angle(0)
    Keyborad_control()
