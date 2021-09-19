import numpy as np

# The environment grid that will contain our robot's surroundings
# Origin is at the top-left corner
class EnvironmentGrid:
    def __init__(self, granularity, sideLength):
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
        self.orientation = 0
    
    # Calculates the number of cells in a row of the
    # environment grid.
    def getNumCellsPerRow(self):
        return int(self.sideLength/self.granularity)
    
    # Creates the container for the environment grid
    def createEnvironmentGrid(self):
        return np.zeros((self.getNumCellsPerRow(), self.numCellsPerRow()))    


    # Calculates x,y position given angle and distance
    # returns a tuple of (xnew,ynew)
    def getPosition(x_init,y_init,angle,dist):
        return ( x_init + dist*np.cos(angle) , y_init + dist*np.sin(angle) )