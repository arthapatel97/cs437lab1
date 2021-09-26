import PositionMessage as pm
import datetime as dt
import time

class PositionLogger():
    def __init__(self):
        self.logs = []

    def append_log(self, log: pm.PositionMessage):
        self.logs.append(log)

    def get_last_log(self):
        return self.logs[-1]

    def __str__(self):
        return_str = ""
        for log in self.logs:
            return_str += str(log)
            return_str += "\n"
        return return_str[0:-1]

logger = PositionLogger()

logger.append_log(pm.PositionMessage(0, (50,50), 0, pm.IDLE))
logger.append_log((pm.PositionMessage(0, (50,50), 70, pm.MOVING_FORWARD)))
time.sleep(2)
logger.append_log((pm.PositionMessage(0, (80,50), 50, pm.TURNING_RIGHT)))
time.sleep(1)
logger.append_log((pm.PositionMessage(-30, (80,50), 60, pm.MOVING_FORWARD)))
time.sleep(3)
logger.append_log((pm.PositionMessage(-30, (130,50), 0, pm.IDLE)))

print(logger)
