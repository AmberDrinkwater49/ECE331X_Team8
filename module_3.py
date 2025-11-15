import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, ndimage
import time
import math
#import adi
import json

num_seconds = 30
# ----------------------------------------------------------
# Code to determine the I/Q data pertaining only to the intented signal.
# Furthermore, the code plots the magnitude and phase components of the I/Q data.
# Finally, the signal constellation is plotted.
#
# Team 8
# Amber Drinkwater, Kaz Coble, Verit Li
# 11-15-2025
# ----------------------------------------------------------
# Deliverables:
# Implement one of the two approaches and capture the resulting raw I/Q data before and after coarse frequency correction.
# Plot the resulting magnitude and phase time-domain plots for the before-and-after data for the chosen approach.
# Plot the signal constellation diagrams of the before-and-after data for the chosen approach.

Fc = (int)(433.9e6) #carrier frequency - original: 433.9e6

bandwidth = 10e5 #Bandwidth of front-end analog filter of RX path original: 10e5
Fs = (int)(521e3) #sampling frequency of ADC in samples per second original: 521e3
buffer_size = (int)(2 ** 12) # previously 2 ** 12
NFFT = 1024 #original: 1024
noverlap = NFFT // 8 #original: 64
FFT_LIMIT = 2500


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

    phases = np.unwrap(np.angle(data)) #convert complex I/Q data to phase (in radians)
    timing = np.linspace(0, time, num=len(data))    
    
    print(timing)
    print(phases)
    plt.plot(timing, phases)
    plt.xlabel("Time (seconds)")
    plt.ylabel("Phase (radians)")
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
    plt.plot(extract_I(data),extract_Q(data),marker='o',linestyle='',color='b',markersize=1)
    plt.xlabel("In-Phase")
    plt.ylabel("Quadrature")
    plt.title("I/Q Signal Constellation")
    plt.grid(True)
    plt.show()

def plot_fft(data):
    fft = np.fft.fft(data)
    # Get the corresponding frequencies
    frequencies = np.fft.fftfreq(len(data), d=1/Fs)

    # Plot the magnitude spectrum (absolute value of the FFT output)
    plt.figure(figsize=(10, 5))
    plt.plot(frequencies, np.abs(fft))
    plt.title('Magnitude Spectrum of the Signal')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.grid(True)
    plt.xlim(0, FFT_LIMIT) # Show only positive frequencies
    plt.show()
    return [fft, frequencies]

# def offsetFinder(data):
# # Estimation of error
#     fftOrder = 2**10
#     k = 1
#     modulationOrder = 2
#     frequencyRange = np.linspace(-Fs/2,Fs/2,fftOrder)
#     # Precalculate constants
#     offsetEstimates = np.zeros(int(np.floor(len(data)/fftOrder)),1)
#     indexToHz = Fs/(modulationOrder*fftOrder)
#     for est in range(1,len(offsetEstimates)):
#         # Increment indexes
#         timeIndex = np.linspace(k,k+fftOrder-1)
#         k = k + fftOrder
#         # Remove modulation effects
#         sigNoMod = data ** modulationOrder
#         # Take FFT and ABS
#         freqHist = np.abs(np.fft.fft(sigNoMod))
#         # Determine most likely offset
#         maxInd = np.argmax(freqHist)
#         offsetInd = maxInd - 1
#         if maxInd>=fftOrder/2: # Compensate for spectrum shift
#             offsetInd = offsetInd - fftOrder
        
#         # Convert to Hz from normalized frequency index
#     offsetEstimates[est] = offsetInd * indexToHz
#     return(offsetEstimates(0))


def find_centroid(fft, frequencies):
    #Integrate over the fft to find the spike where our signal is and determine at which frequency that is!

# Version Textbook
    # fftOrder = 2 ** 10
    # frequencyRange = np.linspace(-Fs/2,Fs/2,fftOrder)
    # offsetEstimates = np.zeros(np.floor(len(fft)/fftOrder),1)
    # offsetIndex = np.argmax(np.abs(fft**2)) - 1
    # indexToHz = Fs/(2*fftOrder)

    # if offsetIndex>=fftOrder/2:
    #     offsetIndex = offsetIndex - fftOrder

    # print(indexToHz*offsetIndex)
    # return offsetIndex*indexToHz

# Version Amber
    sum = 0
    sum2 = 0
    final_freq = 0
    for x in range(0,FFT_LIMIT):
        sum += np.abs(fft[x])
    for x in range(0, FFT_LIMIT):
        sum2 += np.abs(fft[x])
        if sum2 >= sum/2:
            print(frequencies[x])
            return x



def main():
    total_time = 67

    running_std = 0
    signalStart = 0
    signalEnd = 0

    

    raw_data = np.load("samples01.npy")
    '''
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
    '''
    signalStart = 11900000 #11950000
    signalEnd = 12000000   #12000000
    signal_data = raw_data[signalStart:signalEnd]
    signal_time = total_time * (len(signal_data) / len(raw_data))
    
    #plt.specgram(signal_data, Fs=Fs, NFFT=NFFT, noverlap=noverlap, Fc=Fc)

    #plt.savefig('plot.png')
    #plt.show()


    print("image made")
    
    numtaps = 10001
    Fcutoff_low = Fc*0.75
    Fcutoff_high = Fc*1.25
    Fnyquist = Fs/2
    
    #generate low pass filter
    #coeffs = signal.firwin(numtaps,[Fcutoff_low/Fnyquist,Fcutoff_high/Fnyquist],fs=2*Fs,pass_zero=False)
    #convolve the filter and data to apply filter
    [fft, frequencies] = plot_fft(signal_data)
    offset = find_centroid(fft,frequencies)
    impulse = np.zeros(len(signal_data))
    impulse[offset] = 1
    signal_data = np.convolve(signal_data, impulse)

    
    plot_magnitude(signal_data, signal_time)
    plot_phase(signal_data, signal_time)
    plt.specgram(signal_data, Fs=Fs, NFFT=NFFT, noverlap=noverlap, Fc=Fc)
    plt.savefig('plot.png')
    plt.show()
    plot_constellation(signal_data)




main()
