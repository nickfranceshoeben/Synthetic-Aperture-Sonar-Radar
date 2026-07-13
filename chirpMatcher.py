import numpy as np

def matchedFilter(signal, waveform):

    #Inverts and conjugates the emitted waveform to match it with the existing waveform.
    reference = np.conj(
        waveform.signal[::-1]
    )

    return np.convolve(
        signal,
        reference,
        mode="same"
    )