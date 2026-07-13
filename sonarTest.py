import numpy as np
import matplotlib.pyplot as plt

from sonar import Sonar
from waveform import Waveform
from receiver import Receiver
from channel import Channel
from sonarPlatform import Platform
from chirpMatcher import matchedFilter

target = {
    "x": 0,
    "y": 50,
    "reflectivity": 1.0
}

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

wf = Waveform(100e3, 20e3, 1e-3,1e6)

rec = Receiver(1e6, 100, soundSpeed=1500)

rawData = []

for position in platform.positions:

    path = channel.propagationPath(
        position,
        target,
        sonar.carrierFrequency
    )

    rx = rec.createBuffer()

    rec.addEcho(
        rx,
        wf,
        path
    )

    compressed = matchedFilter(rx, wf)
    rawData.append(compressed)




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
for position in platform.positions:

    path = channel.propagationPath(
        position,
        target,
        sonar.carrierFrequency
    )

    phase_history.append(path["phase"])

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


phase_change = np.diff(phase_history)

plt.plot(phase_change)
plt.grid()
plt.show()

#   phase_history = np.unwrap(phase_history)

relative_phase = np.array(phase_history) - phase_history[0]

plt.plot(relative_phase)
plt.xlabel("Ping number")
plt.ylabel("Phase (rad)")
plt.grid()
plt.show()