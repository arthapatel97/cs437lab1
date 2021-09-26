from PositionMessage import *
import datetime as dt
import time

class PositionLogger():
    def __init__(self):
        self.logs = []

    def append_log(self, log: PositionMessage):
        self.logs.append(log)

    def get_last_log(self):
        return self.logs[-1]

    def __str__(self):
        return_str = ""
        for log in self.logs:
            return_str += str(log)
            return_str += "\n"
        return return_str[0:-1]

# logger = PositionLogger()

# logger.append_log(PositionMessage(0, (50,50), 0, IDLE))
# logger.append_log((PositionMessage(0, (50,50), 70, MOVING_FORWARD)))
# time.sleep(2)
# logger.append_log((PositionMessage(0, (80,50), 50, TURNING_RIGHT)))
# time.sleep(1)
# logger.append_log((PositionMessage(-30, (80,50), 60, MOVING_FORWARD)))
# time.sleep(3)
# logger.append_log((PositionMessage(-30, (130,50), 0, IDLE)))

# print(logger)
