import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import time
import adi
import json

num_seconds = 30
# ----------------------------------------------------------
# Code to determine the I/Q data pertaining only to the intented signal.
# Furthermore, the code plots the magnitude and phase components of the I/Q data.
# Finally, the signal constellation is plotted.
#
# Team 8
# Amber Drinkwater, Kaz Coble, Verit Li
# 11-08-2025
# ----------------------------------------------------------
# Deliverables:
#   1. 2 time domain plots showing the magnitude and phase of the intercepted signal
#   2. Explain which modulation scheme is being used, justify with theories from lecture.
#   3. Submit a signal constellation plot, explain whether it matches the theoretical plot.
# ----------------------------------------------------------
# Steps:
#   1. Identify where the signal is active in the time domain
#       a. With a narrow bandwidth, wait for signal beyond some percentage of standard deviation.
#       b. Once the signal drops below some percentage of standard deviation, stop saving data. 
#       Note: It is important to continue calculating the standard deviation so that we don't stop collecting 
#       during a pause in the data.
#   2. Isolate the useful data
#       a. Indexes from part 1 will be saved, the list can then be trimmed.
#   3. Decode the data into magnitude and phase data.
#       a. I believe the datat is already saved this way?
#   4. Plot both as a function of time
#       a. Use matlab library
#   5. Plot mag and phase data on the I/Q plane
#       a. Use numpy real and imaginary functions to split the data and plot using the matlab library

Fc = (int)(433.9e6) #carrier frequency - original: 433.9e6

bandwidth = 10e5 #Bandwidth of front-end analog filter of RX path original: 10e5
Fs = (int)(521e3) #sampling frequency of ADC in samples per second original: 521e3
buffer_size = (int)(2 ** 12) # previously 2 ** 12
NFFT = 1024 #original: 1024
noverlap = NFFT // 8 #original: 64



#raw_data = [0] * ((int)(Fs * num_seconds))
#use numpy zeros, set datatype to complex
raw_data = np.zeros(Fs * num_seconds + (buffer_size-(Fs*num_seconds)%buffer_size), dtype=complex)

def plot_magnitude(data, time):
    #Possibly insert additional code that negates the imaginary part of the complex data?
    
    magnitudes = np.abs(data) #convert complex I/Q data to magnitude
    timing = np.linspace(0, time, num=len(data))    
    
    print(timing)
    print(magnitudes)
    plt.plot(timing, magnitudes)
    plt.xlabel("Time (seconds)")
    plt.ylabel("Magnitude")
    plt.title("Signal Magnitude Plot")
    plt.grid(True)
    plt.show()
    
def plot_phase(data, time):
    #Possibly insert additional code that negates the imaginary part of the complex data?

    phases = np.angle(data) #convert complex I/Q data to phase (in radians)
    phases = np.rad2deg(phases) #degrees-ify
    timing = np.linspace(0, time, num=len(data))    
    
    print(timing)
    print(phases)
    plt.plot(timing, phases)
    plt.xlabel("Time (seconds)")
    plt.ylabel("Phase (degrees)")
    plt.title("Signal Phase Plot")
    plt.grid(True)
    plt.show()
    
def extract_I(data):
    I_array = np.real(data)
    return I_array

def extract_Q(data):
    Q_array = np.imag(data)
    return Q_array

def plot_constellation(data):
    plt.plot(extract_I(data),extract_Q(data),marker='o',linestyle='',color='b',markersize=6)
    plt.xlabel("In-Phase")
    plt.ylabel("Quadrature")
    plt.title("I/Q Signal Constellation")
    plt.grid(True)
    plt.show()

def main():
    total_time = 67

    running_std = 0
    signalStart = 0
    signalEnd = 0



    raw_data = np.load("samples01.npy")

    samplesConsidered = 1e5

    for x in range(int(samplesConsidered), len(raw_data), int(samplesConsidered)):
        currentStd = np.std(raw_data[int(x-samplesConsidered):x]) 
        running_std = np.std(raw_data[:x])
       # print("Current std: " + str(currentStd) + "Running std: " + str(running_std))
        if(running_std != 0 and currentStd > running_std*1.2 and not signalStart):
            signalStart = x
            print("New Start: " + str(x))
        elif(signalStart and currentStd < 0.78*running_std):
            signalEnd = x
            print("New End: " + str(x))


    print("Signal Start: " + str(signalStart))
    print("Signal End: " + str(signalEnd))
    if not signalEnd: signalEnd = len(raw_data)
    
    signal_data = raw_data[signalStart:signalEnd]
    signal_time = total_time * (len(signal_data) / len(raw_data))
    
    plt.specgram(signal_data, Fs=Fs, NFFT=NFFT, noverlap=noverlap, Fc=Fc)

    plt.savefig('plot.png')
    plt.show()


    print("image made")
    
    numtaps = 101
    Fcutoff = Fc
    Fnyquist = Fs/2
    
    #generate low pass filter
    coeffs = signal.firwin(numtaps,Fcutoff/Fnyquist,fs=Fs)
    #convolve the filter and data to apply filter
    signal_data = signal.fftconvolve(coeffs, signal_data)
    
    plot_magnitude(signal_data, signal_time)
    plot_phase(signal_data, signal_time)
    plot_constellation(signal_data)




main()
