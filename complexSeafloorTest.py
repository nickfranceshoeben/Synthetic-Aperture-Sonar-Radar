import numpy as np
import matplotlib.pyplot as plt

from environment import Environment
from sonar import Sonar
from waveform import Waveform
from receiver import Receiver
from channel import Channel
from sonarPlatform import Platform
from chirpMatcher import matchedFilter
from backprojection import createImageGrid, calculateRanges, calculateAllRanges, rangesToSampleIndices, retrieveSamples, backproject

env = Environment()
env.load('complexSeafloor.json')
targets = env.targets

channel = Channel()

platform = Platform(
    startPosition=(0, 0),
    velocity=(2, 0),
    heading=0,
    pingsNumber=100,
    pingInterval=0.5
)

sonar = Sonar(
    carrierFrequency=100e3,
    lookAngle=-np.pi/2 #Pointed downwards
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
            sonar.carrierFrequency,
            sonar.lookAngle
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
    xBounds=(0, 50),
    yBounds=(-50, 10),
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



plt.xlabel("Along-track position x (m)")
plt.ylabel("Across-track position y (m)")
plt.title("Synthetic Aperture Sonar — Backprojection")
plt.colorbar(label="Magnitude")
plt.legend()
plt.show()
