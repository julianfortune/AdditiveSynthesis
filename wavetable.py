#
# wavetable.py
# Created October 23, 2019
#
# author: Julian Fortune
# description:
#

import math
import numpy as np

# Enum for different types of wave shapes
class Shape():
    sin = 0

def createWaveTable(shape, sampleSize):
    if shape == Shape.sin:
        radiansPerSample = 2 * (math.pi) / sampleSize
        radians = [sample * radiansPerSample for sample in range(0, sampleSize)]

        samples = np.sin(radians)
        return samples

# Returns the value for a floating point index to improve wavetable accuracy.
# Uses basic linear interpolation.
def interpolate(previousSample, followingSample, indexFloat):
    return ((indexFloat - int(indexFloat)) * (followingSample - previousSample)
            + previousSample)

# Creates an array of length `sampleLength` representing the sound of a wave
# table played back with a consant `frequency` or varying frequency based on a
# list (also called `frequency` but with type list) recorded at sample rate
# `sampleRate`.
#
# Reference: https://www.music.mcgill.ca/~gary/307/week4/wavetables.html
def generateSound(waveTable, frequencyArray, amplitudeArray, sampleRate, sampleLength):
    waveTableLength = len(waveTable)

    samples = np.empty(sampleLength)

    phaseIncrements = (frequencyArray/sampleRate) * waveTableLength
    phasePosition = 0

    for sampleNumber in range(0, sampleLength):
        phasePosition += phaseIncrements[sampleNumber]

        if phasePosition >= waveTableLength:
            phasePosition -= waveTableLength

        previousIntegerIndex = int(phasePosition)
        followingIntegerIndex = int(phasePosition) + 1

        if followingIntegerIndex >= waveTableLength:
            followingIntegerIndex -= waveTableLength

        previousValue = waveTable[previousIntegerIndex]
        followingValue = waveTable[followingIntegerIndex]

        samples[sampleNumber] = interpolate(previousValue, followingValue,
                                            phasePosition)

    samples = np.multiply(samples, amplitudeArray)

    return samples
