import numpy as np
import sys
import math

# Calculates x,y position given angle and distance
# returns a tuple of (xnew,ynew)
def getPosition(x_origin, y_origin, angle, dist):
    return (x_origin + dist*np.cos(math.radians(angle)), y_origin + dist*np.sin(math.radians(angle)))

# The environment grid that will contain our robot's surroundings
# Origin is at the top-left corner
# The origin of the orientation is parallel to the X-axis, and increasing
# the angle is counter-clockwise, and decreasing the angle is clockwise
class EnvironmentGrid:
    def __init__(self, granularity, sideLength, impactDistance):
        self.initializeEmptyGrid(granularity, sideLength, impactDistance)
    
    # Initializes an empty grid with a certain granularity and sideLength
    def initializeEmptyGrid(self, granularity, sideLength, impactDistance):
        # The size of each square in the environment grid
        # measured in centimeters
        self.granularity = granularity

        # The side length of the entire environment grid
        # measured in centimeters
        self.sideLength = sideLength

        # The container for the environment grid
        # A numpy array where 0 denotes there's nothing there,
        # and 1 denotes there's something there
        self.map = self.createEnvironmentGrid()

        # The start coordinates of our little guy.
        # Places him right in the middle
        self.robotX = self.sideLength/2
        self.robotY = self.sideLength/2

        # The start orientation of our little guy.
        self.RobotOrientation = 0

        # impactDistance is the threshold distance that is considered to be an impact risk
        self.impactDistance = impactDistance

    # Takes the output of the picar as input.
    # scanOutput is a list of tuples, where each tuple
    # contains two values: a degree, and a distance
    # The degree is the degree at which the measurement was taken,
    # and the distance is the recorded distance
    def processScanOutput(self, scanOutput):
        for i in scanOutput:
            degrees = i[0]
            measuredDistance = i[1]
            if (measuredDistance <= self.impactDistance):
                self.recordObstacle(degrees, measuredDistance)

    # Calculates the number of cells in a row of the
    # environment grid.
    def getNumCellsPerRow(self):
        return math.floor(self.sideLength/self.granularity)
    
    # Creates the container for the environment grid
    def createEnvironmentGrid(self):
        return np.zeros((self.getNumCellsPerRow(), self.getNumCellsPerRow()))    

    # Updates the position of the robot
    def updatePosition(self, timeStep, velocity):
        self.robotX, self.robotY = getPosition(self.robotX, self.robotY, self.RobotOrientation, velocity * timeStep)

    # Updates the orientation of the robot
    def updateOrientation(self, timeStep, turnSpeed):
        self.robotOrientation += timeStep*turnSpeed % 360

    # Checks whether the cell is valid
    def isValidCell(self, i, j):
        if (i >= 0 and j >= 0):
            if (i < np.shape(self.map)[0] and j < np.shape(self.map)[1]):
                return True
        return False

    # Marks an object in the environment as an obstacle
    # @ angle: The angle of the object relative to our robot's orientation
    # @ distance: The distance between our robot and the object
    def recordObstacle(self, angle, distance):
        objectX, objectY = getPosition(self.robotX, self.robotY, self.RobotOrientation + angle, distance)
        i, j = self.mapPositionToCell(objectX, objectY)
        if (self.isValidCell(i, j)):
            self.map[i,j] = 1
    
    # Returns the coordinates of a cell after being given the x and y position
    def mapPositionToCell(self, x, y):
        j = math.floor(x/self.granularity)
        i = math.floor(y/self.granularity)
        return [i, j]

# # Testing the environment mapping

# scanOutput = []
# for i in range(90):
#     currentOutput = (45 - i, 20)
#     scanOutput.append(currentOutput)

# testEnvironment = EnvironmentGrid(5, 100, 40)
# testEnvironment.processScanOutput(scanOutput)

# np.set_printoptions(threshold=sys.maxsize)

# print(testEnvironment.map)
