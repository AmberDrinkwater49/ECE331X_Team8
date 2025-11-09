import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import time
import adi
import json

num_seconds = 60
# ----------------------------------------------------------
# Code for generating a spectrogram based on the intermittent
# wireless transmission of AcuRite Wireless Digital Weather Thermometer
# and received by a Pluto SDR
#
# Team 8
# Amber Drinkwater, Kaz Coble, Verit Li
# 10-29-2025
# ----------------------------------------------------------


# ----------------------------------------------------------

# Create radio
sdr = adi.Pluto(uri="ip:192.168.2.1") #default pluto ip address is 192.168.2.1
Fc = (int)(433.9e6) #carrier frequency - original: 433.9e6

bandwidth = 300e3 #Bandwidth of front-end analog filter of RX path original: 10e5
Fs = (int)(1e6) #sampling frequency of ADC in samples per second original: 521e3
buffer_size = (int)(2 ** 14) # previously 2 ** 12
NFFT = 8192 #original: 1024
noverlap = NFFT // 2 #original: 64

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
    time_start = time.time_ns()

    for start in range(0, num_seconds*Fs, buffer_size):
        #print(start)
        end = start + buffer_size
        final_data[start:end] = sdr.rx()
    time_end = time.time_ns()
    
    time_diff = time_end - time_start
    
    print(time_diff)
    
    print("i did da loops")

    plt.specgram(final_data, Fs=Fs, NFFT=NFFT, noverlap=noverlap, Fc=Fc)

    plt.savefig('plot.png')
    plt.show()
    #print("image made")

    np.save('samples', final_data)
    samples = np.load('samples.npy')
    print(samples)

main()
