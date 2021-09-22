import picar_4wd as fc 

def get_enivroment_data(angle_interval=2):
    fc.servo.set_angle(0)
    servo_map = []

    fc.servo.set_angle(fc.max_angle)
    while fc.current_angle >= fc.min_angle:
        fc.current_angle -= angle_interval
        fc.servo.set_angle(fc.current_angle)
        servo_map.append((fc.current_angle, fc.us.get_distance()))
    return servo_map

if __name__ == "__main__":
    print(get_enivroment_data())