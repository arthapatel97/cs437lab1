import numpy
import picar_4wd as fc 
import time

def get_enivroment_data(angle_interval=2):
    servo_map = []
    fc.current_angle = fc.max_angle + angle_interval
    fc.servo.set_angle(fc.max_angle+ angle_interval)
    time.sleep(0.5)
    while fc.current_angle > fc.min_angle:
        fc.current_angle -= angle_interval
        fc.servo.set_angle(fc.current_angle)
        readings_list = []
        for i in range(5):
            readings_list.append(fc.us.get_distance())
        servo_map.append((fc.current_angle, numpy.max(numpy.array(readings_list))))
        time.sleep(0.001)
    return servo_map

if __name__ == "__main__":
    servo_map = get_enivroment_data()
    print(servo_map)
    print(len(servo_map))