#
# additiveSynthesizer.py
# Created October 7, 2019
#
# author: Julian Fortune
# description: Additive Synthesizer class
#

import math
import numpy as np
import matplotlib.pyplot as plt
import wavio

# Local dependencies
from envelope import *

# Enum for different types of wave shapes
class WaveShape():
    sin = 0

class AdditiveSynthesizer():

    waveTable = [float()]
    sampleRate = int() # Samples per second

    parameters = []

    def __init__(self, wave=WaveShape.sin, waveTableLength=512, sampleRate=48000,
        oscillators=1):
        self.waveTable = createWaveTable(wave, waveTableLength)
        self.sampleRate = sampleRate

        for _ in range(0, oscillators):
            parameters.append([Envelope(), Envelope()])

    def generateSound(self, length):
        return generateSoundFromWaveTable(waveTable,
                                          parameters[0][0],
                                          parameters[0][1],
                                          sampleRate,
                                          msToSamples(length, sampleRate))

def createWaveTable(shape, sampleSize):
    if shape == WaveShape.sin:
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
def generateSoundFromWaveTable(waveTable, frequencyArray, amplitudeArray, sampleRate, sampleLength):
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

# Converts value in milliseconds (ms) to samples
def msToSamples(valueInMS, sampleRate):
    return int(valueInMS / 1000 * sampleRate)

def main():
    waveTable = createWaveTable(WaveShape.sin, 512)

    sampleRate = 48000 # Samples per second
    length = 200 # In milliseconds

    frequencyEnvelope = Envelope([[0, 3000],
                                  [msToSamples(2, sampleRate), 200],
                                  [msToSamples(20, sampleRate), 80],
                                  [msToSamples(80, sampleRate), 60],
                                  [msToSamples(100, sampleRate), 30]])

    frequencyEnvelope.length = msToSamples(length, sampleRate)

    amplitudeEnvelope = Envelope([[msToSamples(0.2, sampleRate), 1],
                                  [msToSamples(90, sampleRate), 1]])

    amplitudeEnvelope.length = msToSamples(length, sampleRate)

    sound = generateSoundFromWaveTable(waveTable,
                                      frequencyEnvelope.toArray(),
                                      amplitudeEnvelope.toArray(),
                                      sampleRate,
                                      msToSamples(length,
                                      sampleRate))

    plt.plot(sound)
    plt.show()

    # wavio.write("test.wav", sound, sampleRate, sampwidth=3)

if __name__ == "__main__":
    main()
