import numpy as np


class Waveform:

    def __init__(
        self,
        centerFrequency,
        bandwidth,
        duration,
        samplingFrequency
    ):

        self.fc = centerFrequency
        self.bandwidth = bandwidth
        self.duration = duration
        self.fs = samplingFrequency

        self.signal = self.generateChirp()
        
        
    def generateChirp(self):
        # Chirp is linear, frequency-modulated. 
        
        t = np.arange(
            0,
            self.duration,
            1/self.fs
        )

        k = self.bandwidth / self.duration

        phase = 2*np.pi*(
            self.fc*t
            +
            0.5*k*t**2
        )
        
        # Where k is the chirp rate, equal to bandwith over time. (Increase from lowest to highest frequencies within the bandwidth)

        signal = np.exp(1j*phase)

        return signal