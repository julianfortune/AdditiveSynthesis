#
# envelope.py
# Created October 23, 2019
#
# author: Julian Fortune
# description: Envelope and associated classes
#

import numpy as np
import matplotlib.pyplot as plt

# Local
import conversion

# Class for a point in an envelope
class Point():

    distance = float() # In MS
    value = float()

    def __init__(self, distance= None, value= None):
        self.distance = distance
        self.value = value

# Class for creating an envelope with points
class Envelope():

    points = [Point]

    def __init__(self, pointArray= None):
        if not pointArray: return
        self.points = []

        for pointPair in pointArray:
            self.points.append(Point(distance= pointPair[0],
                                     value= pointPair[1]))

    # Create a 2-d representation of the points for manipulation.
    def asPointArray(self):
        print("Not implemented")

    # Create a 1-d line from point interpolation.
    def toArray(self, sampleRate):
        outputArray = np.empty(0)

        # if len(self.points) > 1:
        for index, point in enumerate(self.points):

            # if point.distance == 0:
            #     outputArray = [point.value]

            # Interpolate up to the first non-zero distance point
            if index == 0 and point.distance > 0:
                # Make linespace
                interpolation = np.linspace(0, point.value,
                                num= conversion.msToSamples(point.distance,
                                                            sampleRate) + 1)
                outputArray = interpolation[:-1]

            # Interpolate from the current point to the next one
            if index < (len(self.points) - 1):
                # Check value of next point and distance to next
                nextPoint = self.points[index+1]
                distanceToNext = (conversion.msToSamples(nextPoint.distance, sampleRate) -
                                  conversion.msToSamples(point.distance, sampleRate))
                # Make linespace
                interpolation = np.linspace(point.value, nextPoint.value,
                                            num= distanceToNext + 1)
                outputArray = np.append(outputArray, interpolation)[:-1]

        outputArray = np.append(outputArray, [self.points[-1].value])

        return outputArray

    def graph(self):
        plt.plot(self.toArray(sampleRate=1000))
        plt.xlabel("Milliseconds")
        plt.show()

def trimOrStretch(arrayToResize, length):
    if len(arrayToResize) >= length:
        return arrayToResize[:length]
    else:
        return np.pad(arrayToResize, (0, length-len(arrayToResize)), mode="edge")
