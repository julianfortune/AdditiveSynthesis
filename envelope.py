#
# Envelope.py
# Created October 7, 2019
#
# author: Julian Fortune
# description: Additive Synthesizer class
#

import numpy as np
import matplotlib.pyplot as plt

# Class for a point in an envelope
class Point():

    distance = int()
    value = int()

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
    def asArray(self):
        print("Not implemented")

    # Create a 1-d line from point interpolation.
    def toArray(self, sampleRate):
        outputArray = np.empty(0)

        for index, point in enumerate(self.points):

            # Interpolate up to the first point if needed
            if index == 0 and point.distance > 0:
                # Make linespace
                interpolation = np.linspace(0, point.value, num= point.distance)
                outputArray = np.append(outputArray, interpolation)

            # Interpolate from the current point to the next one
            if index < (len(self.points) - 1):
                # Check value of next point and distance to next
                nextPoint = self.points[index+1]
                distanceToNext = nextPoint.distance - point.distance
                # Make linespace
                interpolation = np.linspace(point.value, nextPoint.value,
                                            num= distanceToNext)
                outputArray = np.append(outputArray, interpolation)

        return outputArray

    def graph(self):
        plt.plot(self.asArray())
        plt.show()
