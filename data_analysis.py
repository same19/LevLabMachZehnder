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
        start = 16 #for fancy oscilliscope
        # start = 0 #for older oscilliscope
        num = int(rows[8][1]) #for fancy oscilliscope
        # num = int(float(rows[0][1])) #for older oscilliscope
        sample_rate_inverse = float(rows[6][1]) #for fancy oscilliscope
        # sample_rate_inverse = float(rows[1][1]) #for older oscilliscope
        data = [[float(item[i]) for item in rows[start:start + num]] for i in [0,1]] #"i in [0,1]" for fancy oscilliscope, "i in [3,4]" for older oscilliscope
    print(len(data))
    return data

#unwrap data if it wraps around (not working very well)
def unwrap(l, marginUp, marginDown):
    shift = 0
    n = [l[0]]
    for i in range(1,len(l)):
        if (l[i]-l[i-1]) > (wavelength/2 - marginUp):
            shift -= wavelength/2
        if (l[i]-l[i-1]) < -1*(wavelength/2 - marginDown):
            shift += wavelength/2
        n.append(l[i]+shift)
    return n

def processData(data):
    time = data[0]
    A = data[1] #for the old oscilliscope, this is the difference between sensor values, proportional to power. A = 4sqrt(AB)*cos(theta) where theta is phase difference; for new oscilliscope, this is first channel
    # B = data[2] #for new oscilliscope only, second channel
    # diff = np.subtract(A,B) #new oscilliscope only
    diff = A
    
    minV =  np.min(diff)#volts
    maxV =  np.max(diff)#volts
    # minV = -1.1 #can manually set min and max voltages
    # maxV = 0.9

    #theta
    phase = np.arccos(
        np.clip(
            np.multiply(
                np.subtract(diff,np.average(diff)), #center the data
                2/(maxV-minV) #resize the data to fit to [-1,1]
            )
        ,-1,1) #clamp data to [-1,1]
    )
    d = np.multiply(phase, wavelength / (2 * np.pi)) #from phase to path difference = theta/k (where k = 2pi/lambda)
    return [time, d]

def main():
    #plot raw data
    data = retrieveData()
    plt.plot(data[0], data[1])
    plt.show()

    #plot path difference
    newData = processData(data)
    plt.plot(newData[0], newData[1])
    plt.show()

    #the following lines are for attempting to unwrap the data
    # l = []
    # num = 100
    # for i in range(num//2):
    #     l.append(unwrap(newData[1], i*wavelength/num, wavelength/2))
    #     plt.plot(newData[0], l[i])
    # plt.show()
    # avg = np.multiply(np.array(l[0]), 1/(num/2))
    # for j in range(1,num//2):
    #     # print(avg)
    #     # print(np.multiply(l[j], 1/(num/2)))
    #     avg += np.multiply(np.array(l[j]), 1/(num/2))
    # plt.plot(newData[0], avg)
    # plt.show()


    fr = np.fft.rfftfreq(len(newData[1]),d=sample_rate_inverse)
    start_index = 1 #eliminate the asymptotic fourier transform value at 0 Hz
    end_index = len(fr)
    fr = fr[start_index:end_index]
    transform = np.abs(np.fft.rfft(newData[1]))
    amp = np.multiply(transform[start_index:end_index], 2./len(newData[1])) #amplitude, adjusted to match nanometer amplitude for each frequency
    
    plt.plot(fr, amp) #plot raw Fourier transform
    plt.show()
    
    ampScaled = np.divide(amp, np.power(fr, 0.5))
    plt.plot(fr, ampScaled) #graph is in nm/Hz^(1/2) just like Stephen Taylor's thesis
    plt.yscale("log") #log scale
    plt.xscale("log")
    plt.show()

    sum = 0
    for i in range(len(amp)):
        sum += amp[i]

    print(sum)



if __name__=="__main__":
    main()