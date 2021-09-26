import picar_4wd as fc 

def get_enivroment_data(angle_interval=2):
    servo_map = []
    fc.current_angle = fc.max_angle + angle_interval
    while fc.current_angle >= fc.min_angle:
        fc.current_angle -= angle_interval
        fc.servo.set_angle(fc.current_angle)
        servo_map.append((fc.current_angle, fc.us.get_distance()))
    return servo_map

if __name__ == "__main__":
    servo_map = get_enivroment_data()
    print(servo_map)
    print(len(servo_map))