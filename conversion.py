#
# conversion.py
# Created October 23, 2019
#
# author: Julian Fortune
# description:
#

# Converts value in milliseconds (ms) to samples
def msToSamples(valueInMS, sampleRate):
    return int(valueInMS / 1000 * sampleRate)
