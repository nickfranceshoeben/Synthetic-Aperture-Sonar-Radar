import numpy as np

class Platform:

    def __init__(
        self,
        startPosition,
        velocity,
        heading,
        pingsNumber,
        pingInterval
    ):

        self.startPosition = np.array(startPosition, dtype=float)
        self.velocity = np.array(velocity, dtype=float)

        self.heading = heading

        self.pingsNumber = pingsNumber
        self.pingInterval = pingInterval

        self.positions = self.generatePositions()

    def generatePositions(self):

        # Create positions that the platform will take
        positions = []

        for i in range(self.pingsNumber):

            position = (
                self.startPosition
                +
                self.velocity * i * self.pingInterval
            )

            positions.append(position)

        return np.array(positions)
    
    def heading_vector(self):

        return np.array([
            np.cos(self.heading),
            np.sin(self.heading)
        ])