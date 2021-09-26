import datetime as dt

DATETIME_FORMAT = "%a %m/%d/%Y %H:%M:%S"

TURNING_RIGHT = "TURNING_RIGHT"
TURNING_LEFT = "TURNING_LEFT"
MOVING_FORWARD = "MOVING_FORWARD"
MOVING_BACKWARD = "MOVING_BACKWARD"
IDLE = "IDLE"

# def get_meters_per_second():


class PositionMessage():
    def __init__(self, ts, od, p, s, mstate):
        self.timestamp: dt.datetime = ts
        self.orientation_degree = od
        self.position = p
        self.speed = s
        self.move_state = mstate
    
    def __str__(self):
        return "[{}]: ({}, {}) at {} degrees, {} -> powered at {}% ({} m/s)".format(self.timestamp.strftime(DATETIME_FORMAT), self.position[0], self.position[1], self.orientation_degree, self.move_state, self.speed, self.speed)