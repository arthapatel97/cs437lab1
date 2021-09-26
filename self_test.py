import picar_4wd as fc
import time
from threading import *

def speedometer_handler():
    while True:
        print(fc.speed_val())
        time.sleep(0.5)

def fire_up_thread():
    speedometer = Thread(speedometer_handler)

    speedometer.start()

if __name__ == "__main__":
    fire_up_thread()
    # fc.servo.set_angle(fc.min_angle)
    fc.forward(50)
    time.sleep(1)
    fc.backward(60)
    time.sleep(2)
    fc.stop()
    # distance = fc.us.get_distance()
    # print(distance)
    # while True:
    #     fc.servo.set_angle(fc.min_angle)
    #     time.sleep(2)
    #     print("right MIN_ANGLE read: {}".format(fc.us.get_distance()))
    #     fc.servo.set_angle(fc.max_angle)
    #     time.sleep(2)
    #     print("left MAX_ANGLE read: {}".format(fc.us.get_distance()))


