from time import sleep
def power_read():
    from picar_4wd.adc import ADC
    power_read_pin = ADC('A4')
    power_val = power_read_pin.read()
    print(power_val, power_read_pin)

    power_val = (power_val / 4095.0) * 3.3
    # print(power_val)
    power_val = power_val * 3
    power_val = round(power_val, 2)
    return power_val


def main():
    while (True):
        print("battery level: {}".format(power_read()))
        sleep(0.5)


if __name__ == '__main__':
    main()