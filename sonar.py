import numpy as np


class Sonar:

    #Used to indicate sonar orientation relative to the platform. lookAngle is therefore relative to platform heading.

    def __init__(
        self,
        carrierFrequency,
        lookAngle,
        beamWidth=None
    ):

        self.carrierFrequency = carrierFrequency
        self.lookAngle = lookAngle
        self.beamWidth = beamWidth

    def beam_direction(self, heading):

        #Computes absolute angle of the sonar beam

        return heading + self.look_angle