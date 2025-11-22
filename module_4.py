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


