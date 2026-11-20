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

        delaySamples = int(
            path["delay"] * self.fs
        )

        echo = (
            waveform.signal
            *
            path["amplitude"]
            *
            np.exp(1j * path["phase"])
        )

        start = delaySamples
        end = start + len(echo)

        if end <= len(buffer):
            buffer[start:end] += echo
            
