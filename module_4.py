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

def mixer(dds_output, sample):
    return dds_output * sample

def get_phase_error(sample):
    sample = sample ** 2 # BPSK so modulation order = 2
    return 0.5*np.angle(sample)

error_lpf = 0
def lpf(new_error):
    #generate low pass filter
    global error_lpf
    error_lpf = (error_lpf + new_error)/2
    return error_lpf

def update_DDS(new_error):
    dds_input = new_error

def main():
    total_time = 60
    signal_data = np.load("samplesBLE01.npy")
    signal_data = signal_data[:int(len(signal_data)/200)]
    signal_time = total_time * (len(signal_data) / len(signal_data))

    output_data = []

    new_error = get_phase_error(signal_data[0])

    for v in signal_data:
        mixed_v = mixer(DDS(new_error), v)
        output_data.append(mixed_v)
        error = get_phase_error(mixed_v)
        new_error = lpf(error)

    # plot_magnitude(signal_data, signal_time)
    # plot_phase(signal_data, signal_time)
    # plot_constellation(signal_data)

    # plot_magnitude(output_data, signal_time)
    # plot_phase(output_data, signal_time)
    plot_constellation(output_data)


'''

WARNING THIS ALMOST CERTAINLY IS BROKEN SOMEHOW
goal: stabilize the signal constellation
import 3 milllion libraries

read the data from the file

# do the processing steps here
def mixer(dds output, sample):
    return dds output * sample

def get_phase_error(sample):
    #square sample for BPSK or ^4 sample for QPSK you get the idea
    #we're doing ASK here
    return np.angle(sample)

def lpf(error):
    #i dunno do something here get numpy to do it for you I think

dds_current_phase
dds_input
def DDS():
    dds_current_phase = dds_current_phase + dds_input
    return np.exp(-1j*2*pi*dds_current_phase)

def update_dds(new error):
    #add fancy stuff here if you want
    dds_input = new error
    output_data = []

    for v in data:
    mixed_v = mixer(DDS(), v)
    output_data add mixed_v to the end
    error = get_phase_error(sample)
    new_error = lpf(error)
    update_dds(new_error)
    #it's called a DPL LLLLL so maybe you need a loop
    #you need a mixer
    #you need a phase error detector
    #you need a low pass filter
    #DDS (not a dentist) (or some equivalent frequency inator)

plots plots baby
'''
main()