from channel import Channel
from receiver import Receiver
from waveform import Waveform

import matplotlib.pyplot as plt
import numpy as np


channel = Channel()

target = {
    "x": 0,
    "y": 50,
    "reflectivity": 1.0
}

sonarPosition = (0, 0)

path = channel.propagationPath(
    sonarPosition,
    target,
    carrierFrequency=100e3
)

print(path)

wf = Waveform(100e3, 20e3, 1e-3,1e6)

rec = Receiver(1e6, 100, soundSpeed=1500)
rx = rec.createBuffer()
rec.addEcho(rx,wf,path)

# Test second target

target2 = {
    "x": 10,
    "y": 70,
    "reflectivity": 0.5
}

path2 = channel.propagationPath(sonarPosition, target2, carrierFrequency=100e3)

rec.addEcho(rx,wf,path2) #Add echo of second target





plt.figure(figsize=(10,4))

plt.plot(
    np.abs(rx)
)

plt.xlabel("Sample")
plt.ylabel("Amplitude")

plt.grid()

plt.show()

# Expected echo location
echoTime = 2 * 50 / 1500   # seconds
echoSample = int(echoTime * 1e6)

# Look at a small window around the echo
window = 200

segment = rx[
    echoSample-window:
    echoSample+window
]

plt.figure(figsize=(10,4))

plt.plot(np.real(segment), label="Real")
plt.plot(np.imag(segment), label="Imaginary")

plt.xlabel("Sample")
plt.ylabel("Amplitude")
plt.legend()
plt.grid()

plt.show()

phase = np.angle(segment)


unwrappedPhase = np.unwrap(phase)

plt.plot(unwrappedPhase)
plt.xlabel("Sample")
plt.ylabel("Unwrapped phase (rad)")
plt.grid()

plt.show()