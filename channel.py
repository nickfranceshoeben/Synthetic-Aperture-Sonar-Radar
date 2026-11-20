import numpy as np

class Channel:


    def __init__(self,speedOfSound=1500):
        
        self.c = speedOfSound
        
    
    def range(self, platformPosition, target):
        
        dx = target["x"] - platformPosition[0]
        dy = target["y"] - platformPosition[1]
        
        return np.sqrt(dx**2 + dy**2)
    
    def delay(self,R):
        
        return 2*R/self.c
    
    def angle(self, platformPosition, target):
        # Measures angle between the positive y-axis and the target.
        dx = target["x"] - platformPosition[0]
        dy = target["y"] - platformPosition[1]

        return np.arctan2(dx, dy)
    
    def beamGain(self, theta, exponent=8):
        # Simple beam, quite narrow at exponent 8
        gain = max(0.0, np.cos(theta))
        return gain ** exponent
    
    def spreadingLoss(self, R):

        return 1 / R
    
    def phase(self, R, carrierFrequency):

        wavelength = self.c / carrierFrequency

        return -4 * np.pi * R / wavelength
    
    def propagationPath(
    self,
    platformPosition,
    target,
    carrierFrequency):
        
        # Returns a dict with all relevant channel variables
        
        R = self.range(platformPosition,target)
        delay = self.delay(R)
        angle = self.angle(platformPosition, target)
        gain = self.beamGain(angle)
        loss = self.spreadingLoss(R)
        phase = self.phase(R, carrierFrequency)
        
        amplitude = (
        target["reflectivity"]
        * gain
        * loss
                    )
        
        return {
        "delay": delay,
        "amplitude": amplitude,
        "phase": phase
        }
        
        
        
                