import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, ndimage
import time
import math
#import adi
import json

# Team 8
# Amber Drinkwater, Kaz Coble, Verit Li
# 11-22-2025
# ----------------------------------------------------------
# Deliverables:
#   1. Implement a DPLL that intercepts the OTA BPSK transmission at the 915MHz carrier frequency
#   2. Once you have a solution that obtains a "lock" on your phase, plot the "before" and "after" 
#       signal constellation diagrams, where the "before" plot shows the ring that is characteristic 
#       of a signal with phase rotation and the "after" plot shows two clearly defined signal constellation 
#       points (albeit fuzzy due to additive noise in the transmission environment).
#   3. Also show a plot of the phase error as a function of time. 
#       This plot should have some level of oscillation at first but then converge 
#       to an asymptote, indicating a "lock" on the phase.
# ----------------------------------------------------------
# Steps:
#   1.
#
#
#
#
FFT_LIMIT = 2500
Fs = (int)(521e3) #sampling frequency of ADC in samples per second original: 521e3


def plot_magnitude(data, time):
    
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

    phases = np.angle(data) #convert complex I/Q data to phase (in radians)
    phases = np.unwrap(phases) #unwrap makes it so there are no discontinuities caused by going from pi to -pi 
    #phases = np.rad2deg(phases) #degrees-ify
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

dds_current_phase = 0
def DDS(dds_input):
    global dds_current_phase
    dds_current_phase = dds_current_phase + dds_input
    return np.exp(-1j*dds_current_phase)

#simply mixes the sample and output
def mixer(dds_output, sample):
    return dds_output * sample

def get_phase_error(sample):
    sample = sample ** 2 # BPSK so modulation order = 2
    #divide by the modulation order as well when returning the angle
    return 0.5*np.angle(sample)

error_lpf = 0
def lpf(new_error, Kp, Ki):
    #generate low pass filter
    global error_lpf
    #a running average acts as the lowpass filter
    error_lpf = (error_lpf + new_error)/2
    return Kp*new_error + Ki*error_lpf

def plot_fft(data):
    fft = np.fft.fft(data)
    # Get the corresponding frequencies
    frequencies = np.fft.fftfreq(len(data), d=1/Fs)

    # Plot the magnitude spectrum (absolute value of the FFT output)
    # plt.figure(figsize=(10, 5))
    # plt.plot(frequencies, np.abs(fft))
    # plt.title('Magnitude Spectrum of the Signal')
    # plt.xlabel('Frequency (Hz)')
    # plt.ylabel('Magnitude')
    # plt.grid(True)
    # plt.xlim(0, FFT_LIMIT) # Show only positive frequencies
    # plt.show()
    return [fft, frequencies]

def find_centroid(fft, frequencies):
    #Integrate over the fft to find the spike where our signal is and determine at which frequency that is!
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
            print(x)
            return frequencies[int(x)]
    return 0

def main():
    signal_data = np.load("samplesBLE01.npy")
    #normalize the data
    signal_data = signal_data / np.mean(np.abs(signal_data))


    [fft, frequencies] = plot_fft(signal_data)
    offset = find_centroid(fft,frequencies)
    Fo = offset
    #Fo=700
    N = len(signal_data)
    n = np.arange(N)               # sample index array
    t = n / Fs                     # time base
    
    signal_data = signal_data * (math.e**(-1j*2*np.pi*Fo*t))


    output_data = []

    #Values for PI control
    Kp = 1
    Ki = 0.02

    new_error = get_phase_error(signal_data[0])


    #iterate through all of the data
    for v in range(len(signal_data)):
        mixed_v = mixer(DDS(new_error), signal_data[v])
        error = get_phase_error(mixed_v)
        new_error = lpf(error, Kp, Ki)
        #To determine when the lock is acheived
        #the values here were determined based mostly on trial and error, we started from what the last error value was and then went down in orders of magnitude.
        if abs(error) < 0.00001 and v > 100:
            # adding only values that are below a certain error threshold
            output_data.append(mixed_v)


    #before
    plot_constellation(signal_data)
    #after
    plot_constellation(output_data)

main()