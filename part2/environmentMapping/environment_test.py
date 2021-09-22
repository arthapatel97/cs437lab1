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

    return testEnvironment

if __name__ == "__main__":
    print(getMap())