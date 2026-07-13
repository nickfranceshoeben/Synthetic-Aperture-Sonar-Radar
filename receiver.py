import numpy as np

class Receiver:
    
    def __init__(self, samplingFrequency, maxRange, soundSpeed):
        
        self.fs = samplingFrequency
        self.maxrange = maxRange
        self.c = soundSpeed
        
        self.listenTime = 2*maxRange / soundSpeed
        
    def createBuffer(self):

        # Creates an empty recording for a given position
        
        nSamples = int(
            self.listenTime * self.fs
        )

        return np.zeros(
            nSamples,
            dtype=np.complex64 # No need for double precision complex, will save memory in larger simulations
        )
        
    def addEcho(
    self,
    buffer,
    waveform,
    path
    ):
        
        # Simulates a target's signal at the receiver based on waveform and channel.

        delaySamples = path["delay"] * self.fs

        integerDelay = int(delaySamples)

        fractionalDelay = delaySamples - integerDelay

        delayPhase = np.exp(
            -1j * 2*np.pi * waveform.fc * path["delay"]
)

        echo = (
            waveform.signal
            *
            path["amplitude"]
            *
            np.exp(1j * path["phase"])
            * delayPhase
        )

        start = integerDelay

        buffer[start:start+len(echo)] += (
            echo * (1 - fractionalDelay)
        )

        buffer[start+1:start+len(echo)+1] += (
            echo * fractionalDelay
        )
            
