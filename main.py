import matplotlib.pyplot as plt
import numpy as np

from environment import Environment
from waveform import Waveform


'''Waveform tests:

waveform = Waveform(
    100e3,
    20e3,
    1e-3,
    1e6
)

plt.plot(
    np.real(waveform.signal)
)

plt.xlabel("Sample")
plt.ylabel("Amplitude")
plt.show()


# Fourier transform
spectrum = np.fft.fft(waveform.signal)

# Frequency axis
freqs = np.fft.fftfreq(
    len(waveform.signal),
    1 / waveform.fs
)

# Shift zero frequency to the centre
spectrum = np.fft.fftshift(spectrum)
freqs = np.fft.fftshift(freqs)

# Plot magnitude
plt.figure(figsize=(8, 4))
plt.plot(
    freqs / 1e3,
    20 * np.log10(np.abs(spectrum))
)

plt.xlabel("Frequency (kHz)")
plt.ylabel("Magnitude (dB)")
plt.grid(True)
plt.show()

'''


'''Environment tests:
env = Environment()
env.load()
env.plot()

'''