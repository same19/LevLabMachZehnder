import numpy as np
from matplotlib import pyplot as plt
import math

#time, intensity, intensityRefA, intensityRefB
data = [
    [0,1,2,3,4,5,6,7,8],
    [1, 1, 0.5, 0.7, 0, 2.0, 3.0, 2.0, 2.0],
    [0.7,0.7,0.7,0.7,0.7,0.7,0.7,0.7,0.7],
    [0.95,0.95,0.95,0.95,0.95,0.95,0.95,0.95,0.95]
]
wavelength = 780 #nanometers

def retrieveData():
    return []

def processData(data):
    time = [i[0] for i in data]
    intensity = [i[1] for i in data]
    A = [i[2] for i in data]
    B = [i[3] for i in data]
    phase = np.arccos(
        np.multiply(
            np.subtract(
                np.subtract(intensity, A),
                B
            ),
            np.power(
                np.multiply(
                    2,
                    np.multiply(A,B)
                ),
                -1
            )
        )
    )
    d = np.multiply(phase, wavelength / (2 * np.pi))
    """
    amp = sqrt(a^2 + b^2 + 2abcos(phase shift))
    phase shift = arccos((I - A - B)/(2ab))
    
    """
    return [time, d]

def main():
    processData(data)
    plt.plot(data[0], data[1])
    plt.show()


if __name__=="__main__":
    main()