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

        self.signal = self.generateBasebandChirp()
        
        
    def generateChirp(self):
        # RF-Frequency chirp. Chirp is linear, frequency-modulated. 
        
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
    
    def generateBasebandChirp(self):
        #Had a run-in with the Nyquist theorem; baseband chirp overcomes the issue.
        
        t = np.arange(0, self.duration, 1/self.fs)
        k = self.bandwidth / self.duration

        phase = 2*np.pi*(0.5*k*t**2)
        signal = np.exp(1j*phase)

        return signal