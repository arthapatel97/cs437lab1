import picar_4wd as fc
import time

if __name__ == "__main__":
    fc.servo.set_angle(fc.min_angle)
    fc.forward(100)
    time.sleep(2)
    fc.stop()
    distance = fc.us.get_distance()
    print(distance)
    while True:
        fc.servo.set_angle(fc.min_angle)
        time.sleep(2)
        print("right MIN_ANGLE read: {}".format(fc.us.get_distance()))
        fc.servo.set_angle(fc.max_angle)
        time.sleep(2)
        print("left MAX_ANGLE read: {}".format(fc.us.get_distance()))


