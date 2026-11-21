import numpy as np

def matchedFilter(signal, waveform):

    reference = np.conj(waveform.signal[::-1])

    return np.convolve(signal, reference, mode="full")