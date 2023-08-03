import numpy as np
from matplotlib import pyplot as plt
import math
import os
import csv

wavelength = 780 #nanometers
minV =  1.8#volts
maxV =  2.2#volts

def retrieveData():
    data = []
    directory = "raw_data"
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        with open(f) as csvfile:
            rows = list(csv.reader(csvfile))
            start = 16
            num = int(rows[8][1])
            data = [[float(item[i]) for item in rows[start:start + num]] for i in range(5)]
        break
    return data

def processData(data):
    time = [i[0] for i in data]
    # intensity = [i[1] for i in data]
    A = [i[1] for i in data]
    B = [i[2] for i in data]
    phase = np.arccos(
        np.multiply(
            np.subtract(
                A,
                B
            ),
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


if __name__=="__main__":
    main()