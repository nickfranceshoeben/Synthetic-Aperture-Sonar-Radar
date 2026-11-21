import numpy as np
import matplotlib.pyplot as plt

from sonar import Sonar
from waveform import Waveform
from receiver import Receiver
from channel import Channel
from sonarPlatform import Platform
from chirpMatcher import matchedFilter
from backprojection import createImageGrid, calculateRanges, calculateAllRanges, rangesToSampleIndices, retrieveSamples, backproject

targets = [
    {"x": 0, "y": 50, "reflectivity": 1.0},
    {"x": 0, "y": 50.35, "reflectivity": 1.0}
]
channel = Channel()

platform = Platform(
    startPosition=(-50, 0),
    velocity=(2, 0),
    heading=0,
    pingsNumber=100,
    pingInterval=0.5
)

sonar = Sonar(
    carrierFrequency=100e3,
    lookAngle=np.pi/2
)

wf = Waveform(10e3, 20e3, 1e-3,100e3)

rec = Receiver(100e3, 100, soundSpeed=1500)

rawData = []


for position in platform.positions:
    
    rx = rec.createBuffer()
    
    for target in targets:
        path = channel.propagationPath(
            position,
            target,
            sonar.carrierFrequency
        )

        rec.addEcho(
            rx,
            wf,
            path
        )
        

    compressed = matchedFilter(rx, wf)
    rawData.append(compressed)    
    peakIndex = np.argmax(np.abs(compressed))
    
rawData = np.array(rawData)
    
X, Y = createImageGrid(
    xBounds=(-50, 50),
    yBounds=(0, 100),
    xPixels=801,
    yPixels=801
)

ranges = calculateAllRanges(X, Y, platform.positions)

sampleIndices = rangesToSampleIndices(ranges,rec.fs,channel.c, len(wf.signal))

samples = retrieveSamples(rawData, sampleIndices)

image = backproject(
    samples,
    ranges,
    sonar.carrierFrequency,
    channel.c
)

print(ranges.shape)
print(sampleIndices.shape)
print(samples.shape)

plt.figure(figsize=(10, 8))

plt.imshow(
    np.abs(image),
    extent=[X.min(), X.max(), Y.min(), Y.max()],
    origin="lower",
    aspect="auto",
    cmap="viridis"
)

plt.scatter(0, 50, color="red", marker="x", label="Actual target")

plt.xlabel("Along-track position x (m)")
plt.ylabel("Across-track position y (m)")
plt.title("Synthetic Aperture Sonar — Backprojection")
plt.colorbar(label="Magnitude")
plt.legend()
plt.show()
    
'''




rawData = np.array(rawData)

peakHistory = []

for compressed in rawData:
    peakHistory.append(
        np.argmax(np.abs(compressed))
    )

plt.plot(peakHistory)
plt.grid()
plt.show()
phase_history = []
'''

'''
for position in platform.positions:

    path = channel.propagationPath(
        position,
        target,
        sonar.carrierFrequency
    )

    phase_history.append(path["phase"])

'''

'''
phase_history = []

for position, compressed in zip(
        platform.positions,
        rawData):

    R = channel.range(
        position,
        target
    )

    delay = channel.delay(R)

    sample = int(delay * rec.fs + len(wf.signal)//2)

    window = compressed[sample-3:sample+4]

    phase_history.append(
        np.angle(np.sum(window))
    )
    
'''
'''
for ping in rawData:

    peak = np.argmax(
        np.abs(ping)
    )

    phase_history.append(
        np.angle(
            ping[peak]
        )
    )

    '''


'''phase_change = np.diff(phase_history)

plt.plot(phase_change)
plt.grid()
plt.show()

#   phase_history = np.unwrap(phase_history)

relative_phase = np.array(phase_history) - phase_history[0]

plt.plot(relative_phase)
plt.xlabel("Ping number")
plt.ylabel("Phase (rad)")
plt.grid()
plt.show()'''