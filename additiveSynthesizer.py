#
# additiveSynthesizer.py
# Created October 7, 2019
#
# author: Julian Fortune
# description: Additive Synthesizer class
#

import numpy as np
import matplotlib.pyplot as plt
import wavio

# Local dependencies
import envelope
import conversion
import wavetable

# TODO:
# - Make sustain/early cut-off work for envelopes in oscillator

class AdditiveSynthesizer():

    waveTable = [float()]
    sampleRate = int() # Samples per second

    parameters = []

    def __init__(self, wave=wavetable.Shape.sin, waveTableLength=512,
        sampleRate=48000, oscillators=1):
        self.waveTable = wavetable.createWaveTable(wave, waveTableLength)
        self.sampleRate = sampleRate

        for _ in range(0, oscillators):
            self.parameters.append([envelope.Envelope(), envelope.Envelope()])

    def generateSound(self, duration):
        lengthInSamples = conversion.msToSamples(duration, self.sampleRate)

        sound = None

        for oscillatorParameters in self.parameters:
            frequencyEnvelope = oscillatorParameters[0].toArray(self.sampleRate)
            amplitudeEnvelope = oscillatorParameters[1].toArray(self.sampleRate)

            frequencyEnvelope = envelope.trimOrStretch(frequencyEnvelope,
                                                       lengthInSamples)
            amplitudeEnvelope = envelope.trimOrStretch(amplitudeEnvelope,
                                                       lengthInSamples)

            samples = wavetable.generateSound(self.waveTable, frequencyEnvelope,
                                              amplitudeEnvelope, self.sampleRate,
                                              lengthInSamples)

            if sound is not None:
                sound = np.add(sound, samples)
            else:
                sound = samples

        # Normalize (keep within range(-1,1))
        # Source: https://stackoverflow.com/questions/1735025/how-
        # to-normalize-a-numpy-array-to-within-a-certain-range
        sound /= np.max(np.abs(sound), axis=0)

        return sound

def main():
    synth = AdditiveSynthesizer()

    osc1 = [envelope.Envelope(pointArray=[[0,400]]),
            envelope.Envelope(pointArray=[[0,1], [400, 0]])]
    osc2 = [envelope.Envelope(pointArray=[[0,800]]),
            envelope.Envelope(pointArray=[[0,1], [200, 0]])]
    osc3 = [envelope.Envelope(pointArray=[[0,1600]]),
            envelope.Envelope(pointArray=[[0,1], [20, 0.3], [50, 0]])]

    synth.parameters = [osc1, osc2, osc3]
    sound = synth.generateSound(duration= 1000)

    wavio.write("test.wav", sound, synth.sampleRate, sampwidth=3)

    # plt.plot(sound)
    # plt.show()

if __name__ == "__main__":
    main()
