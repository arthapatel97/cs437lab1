import picar_4wd as fc
import time
from threading import *

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

if __name__ == "__main__":
    fc.start_speed_thread()
    fire_up_thread()
    # fc.servo.set_angle(fc.min_angle)
    fc.forward(10)
    time.sleep(1)
    fc.forward(10)
    time.sleep(1)
    fc.forward(10)
    time.sleep(1)
    fc.backward(10)
    time.sleep(1)
    fc.backward(10)
    time.sleep(1)
    fc.backward(10)
    time.sleep(1)
    fc.stop()
    running = 1


