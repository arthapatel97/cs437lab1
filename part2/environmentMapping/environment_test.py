import environmentGrid as env
import uv_scan as sam
import numpy as np
from PIL import Image

GRANULARITY = 5
SIDE_LENGTH = 200
IMPACT_DISTANCE = 200

def getMap(granularity=GRANULARITY, sideLength=SIDE_LENGTH, impactDistance=IMPACT_DISTANCE):
    # Sam, put the output of your function here
    scanOutput = sam.get_enivroment_data(2)
    print(scanOutput)

    testEnvironment = env.EnvironmentGrid(granularity, sideLength, impactDistance)
    testEnvironment.processScanOutput(scanOutput)

    # added as per Sam's request <3
    map = testEnvironment.map
    middle = np.int(np.shape(map)[0]/2)
    map[middle, middle] = 1
    map = map * 255

    im = Image.fromarray(map)
    im = im.resize((500, 500))
    im.show()

    return map

if __name__ == "__main__":
    getMap()