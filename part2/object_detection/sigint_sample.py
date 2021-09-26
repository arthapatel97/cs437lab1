from time import sleep
import signal
import sys

def signal_handler(sig, frame):
    print("interrupt")

    sys.exit(0)


def main():
    while True:
        print("nice")
        sleep(1)
    return;

signal.signal(signal.SIGINT, signal_handler)


if __name__ == '__main__':
    main()