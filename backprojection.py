import numpy as np



def createImageGrid(xBounds, yBounds, xPixels, yPixels):

    #Creates an array with dimensions (N_pings, Ny, Nx), where y and x are pixel positions for the reconstructed image.
    x = np.linspace(xBounds[0], xBounds[1], xPixels)
    y = np.linspace(yBounds[0], yBounds[1], yPixels)

    X, Y = np.meshgrid(x, y)

    return X,Y

def calculateRanges(X, Y, platformPosition):

    #Vectorised computation of range from given point to sample position.
    dx = X - platformPosition[0]
    dy = Y - platformPosition[1]

    ranges = np.sqrt(dx**2 + dy**2)

    return ranges

def calculateAllRanges(X, Y, platformPositions):
    
    #Vectorised computation of range from each point sampled to the platform position.
    dx = X[np.newaxis, :, :] - platformPositions[:, 0, np.newaxis, np.newaxis]
    dy = Y[np.newaxis, :, :] - platformPositions[:, 1, np.newaxis, np.newaxis]

    ranges = np.sqrt(dx**2 + dy**2)

    return ranges

def rangesToSampleIndices(ranges, samplingFrequency, soundSpeed, waveformLength):
    #For a given pixel and ping, compute the sample index at which an echo might be found.
    delays = 2 * ranges / soundSpeed

    sampleIndices = (
        delays * samplingFrequency
        + waveformLength - 1 #-1 accounts for the matched filter shift by 1.
    )

    return sampleIndices

def retrieveSamples(rawData, sampleIndices):

    indices = np.rint(sampleIndices).astype(int)

    valid = (
        (indices >= 0)
        & (indices < rawData.shape[1])
    ) #Check that pixel doesn't correspond to echo outside the buffer - within max range only.

    indices = np.clip(indices, 0, rawData.shape[1] - 1)

    pingIndices = np.arange(rawData.shape[0])[:, None, None]

    samples = rawData[pingIndices, indices]

    samples[~valid] = 0 #~ := NOT operator on array. 

    return samples

def compensatePhase(samples, ranges, carrierFrequency, soundSpeed):
    wavelength = soundSpeed / carrierFrequency
    phase = -4 * np.pi * ranges / wavelength

    compensated = samples * np.exp(-1j * phase)

    return compensated

def backproject(samples, ranges, carrierFrequency, soundSpeed):
    compensated = compensatePhase(
        samples, ranges, carrierFrequency, soundSpeed
    )

    image = np.sum(compensated, axis=0)

    return image