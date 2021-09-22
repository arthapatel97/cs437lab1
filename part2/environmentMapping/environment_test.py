import environmentGrid as env
import uv_scan as sam
import numpy as np

GRANULARITY = 5
SIDE_LENGTH = 90
IMPACT_DISTANCE = 40

def getMap(granularity=GRANULARITY, sideLength=SIDE_LENGTH, impactDistance=IMPACT_DISTANCE):
    # Sam, put the output of your function here
    scanOutput = sam.get_enivroment_data(1)

    testEnvironment = env.EnvironmentGrid(granularity, sideLength, impactDistance)
    testEnvironment.processScanOutput(scanOutput)

    # added as per Sam's request <3
    map = testEnvironment.map
    middle = np.int(np.shape(map)[0]/2)
    print(middle)
    map[middle, middle] = -2

    return map

if __name__ == "__main__":
    print(getMap())