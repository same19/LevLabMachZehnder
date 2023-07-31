import numpy as np
from matplotlib import pyplot as plt
import math

data = [] #time: intensity
wavelength = 780 #nanometers

def processData(data):
    time = [i[0] for i in data]
    intensity = [i[1] for i in data]
    phase = np.multiply(2, np.arccos(np.sqrt(np.multiply(0.25, intensity))))
    d = np.multiply(phase, wavelength / (2 * np.pi))
    """
    phase = 0: intensity = 2*single
    phase = 90: 
    phase = 180:
    sina + sinb = 2sin((a+b)/2)cos((a-b)/2)
    -> sin(x) + sin(x+theta) = 2sin(x+theta/2)cos(theta/2)
    -> amplitude of new wave is 2cos(theta/2)
    -> intensity of new wave is 4cos^2(theta/2)
    -> if we have the new wave's intensity J, and the base wave's intensity I, then the phase shift is 2 * arccos(sqrt(J/4)) which will be in 0 to pi radians
    
    """
    return [time, d]

def main():
    return


if __name__=="__main__":
    main()