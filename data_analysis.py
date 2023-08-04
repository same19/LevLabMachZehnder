import numpy as np
from matplotlib import pyplot as plt
import math
import os
import csv

wavelength = 780 #nanometers
filename = "TEK00011.CSV"

def retrieveData():
    global sample_rate_inverse
    data = []
    directory = "raw_data"
    f = os.path.join(directory, filename)
    with open(f) as csvfile:
        rows = list(csv.reader(csvfile))
        start = 16
        num = int(rows[8][1])
        sample_rate_inverse = float(rows[6][1])
        data = [[float(item[i]) for item in rows[start:start + num]] for i in range(2)]
    return data

def processData(data):
    time = data[0]
    # intensity = [i[1] for i in data]
    A = data[1]
    
    minV =  np.min(A)#volts
    maxV =  np.max(A)#volts
    print(minV)
    print(maxV)

    # B = [i[2] for i in data]
    phase = np.arccos(
        np.multiply(
            A,
            1/(maxV-minV)
        )
    )
    d = np.multiply(phase, wavelength / (2 * np.pi))
    return [time, d]

def main():
    data = retrieveData()
    newData = processData(data)
    plt.plot(newData[0], newData[1])
    plt.show()
    fr = np.fft.rfftfreq(len(newData[1]),d=sample_rate_inverse)
    start_index = 1
    fr = fr[start_index:]
    amp = np.multiply(np.abs(np.fft.rfft(newData[1])), 2./len(newData[1]))[start_index:]
    ampFit = np.multiply(np.power(fr, -1),42.4044555918)
    plt.plot(fr, amp)
    plt.plot(fr, ampFit)
    plt.show()
    plt.plot(fr, np.subtract(amp,ampFit))
    plt.show()


if __name__=="__main__":
    main()