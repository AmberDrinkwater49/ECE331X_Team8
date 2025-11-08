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

# Create radio
sdr = adi.Pluto(uri="ip:192.168.2.1") #default pluto ip address is 192.168.2.1
Fc = (int)(433.9e6) #carrier frequency
bandwidth = 10e5 #Bandwidth of front-end analog filter of RX path
Fs = (int)(521e3) #sampling frequency of ADC in samples per second
buffer_size = (int)(2 ** 12)

# Configure properties
sdr.rx_rf_bandwidth = (int)(bandwidth) #Bandwidth of front-end analog filter of RX path
                      #max of 20MHz for AD9363
                      #will we have to limit bandwidth further bc data limitations?

sdr.rx_sample_rate = Fs #Sample rate RX and TX paths in samples per second
                            #max of 61440000 S/s (61.44 MS/s)
sdr.rx_lo =(int)(Fc) #Carrier frequency of RX path (433.9 MHz)

sdr.gain_control_mode_chan0 = "manual" #Mode of receive path AGC(Automatic Gain Control).
#Options are: slow_attack, fast_attack, manual
#slow_attack is for when the signal you are receiving has gradually changing power levels
#while fast_attack is for rapidly changing power levels

sdr.rx_hardwaregain_chan0 = 50
#sdr gain 50


# Configuration of data channel unneeded
sdr.rx_enabled_channels = [0] #enable only one rx channel
sdr.rx_buffer_size =  buffer_size  #Size of receive buffer in samples


#final_data = [0] * ((int)(Fs * num_seconds))
#use numpy zeros, set datatype to complex
final_data = np.zeros(Fs * num_seconds + (buffer_size-(Fs*num_seconds)%buffer_size), dtype=complex)

'''
def dataCapture() -> list:
    #This function begins the capture of data at given frequencies to decode the thermometers
    data = sdr.rx()
    Rx_0 = data
    return Rx_0
'''

def main():
    for start in range(0, num_seconds*Fs, buffer_size):
        #print(start)
        end = start + buffer_size
        final_data[start:end] = sdr.rx()
    print("i did da loops")

    plt.specgram(final_data, Fs=Fs, NFFT=256, noverlap=64, Fc=Fc)

    #plt.savefig('plot.png')
    plt.show()
    print("image made")

    np.save('samples', final_data)
    samples = np.load('samples.npy')
    print(samples)

main()
