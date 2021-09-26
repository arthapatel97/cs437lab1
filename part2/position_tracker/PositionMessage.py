import datetime as dt

DATETIME_FORMAT = "%a %m/%d/%Y %H:%M:%S"

TURNING_RIGHT = "TURNING_RIGHT"
TURNING_LEFT = "TURNING_LEFT"
MOVING_FORWARD = "MOVING_FORWARD"
MOVING_BACKWARD = "MOVING_BACKWARD"
IDLE = "IDLE"

# def get_meters_per_second():

class PositionMessage():
    def __init__(self, orientation_degree, position, speed, mstate):
        self.timestamp: dt.datetime = dt.datetime.now()
        self.orientation_degree = orientation_degree
        self.position = position
        self.speed = speed
        self.move_state = mstate
    
    def __str__(self):
        return "[{}]: ({}, {}) at {} degrees, {} -> powered at {}% ({} m/s)".format(self.timestamp.strftime(DATETIME_FORMAT), self.position[0], self.position[1], self.orientation_degree, self.move_state, self.speed, self.speed)