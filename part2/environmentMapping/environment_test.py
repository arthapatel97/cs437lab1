import environmentGrid as env
import uv_scan as usv
import numpy as np

GRANULARITY = 5
SIDE_LENGTH = 100
IMPACT_DISTANCE = 4000

def getMap(granularity=GRANULARITY, sideLength=SIDE_LENGTH, impactDistance=IMPACT_DISTANCE):
    # Sam, put the output of your function here
    scanOutput = usv.get_enivroment_data()

    testEnvironment = env.EnvironmentGrid(granularity, sideLength, impactDistance)
    testEnvironment.processScanOutput(scanOutput)

    return testEnvironment

if __name__ == "__main__":
    print(getMap())