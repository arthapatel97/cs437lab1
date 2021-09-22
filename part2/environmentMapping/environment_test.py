import environmentGrid as env
import numpy as np

GRANULARITY = 5
SIDE_LENGTH = 100
IMPACT_DISTANCE = 40

def getMap(granularity=GRANULARITY, sideLength=SIDE_LENGTH, impactDistance=IMPACT_DISTANCE):
    # Sam, put the output of your function here
    scanOutput = []

    testEnvironment = env.EnvironmentGrid(granularity, sideLength, impactDistance)
    testEnvironment.processScanOutput(scanOutput)

    # added as per Sam's request <3
    map = testEnvironment.map
    middle = np.floor(np.shape(map)[0]/2)
    map[middle, middle] = -2

    return map

if __name__ == "__main__":
    print(getMap())