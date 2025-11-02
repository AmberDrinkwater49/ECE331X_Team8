import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import time
import adi

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
sdr = adi.ad9363(uri="ip:192.168.2.1") #default pluto ip address is 192.168.2.1
Fc = 433.9e6 #center frequency
bandwidth = 10e6 #Bandwidth of front-end analog filter of RX path
Fm = bandwidth/2
Fs = 6e6 #sampling frequency of ADC in samples per second


# Configure properties
sdr.rx_rf_bandwidth = bandwidth #Bandwidth of front-end analog filter of RX path
                      #max of 20MHz for AD9363
                      #will we have to limit bandwidth further bc data limitations?

sdr.sample_rate = Fs #Sample rate RX and TX paths in samples per second
                            #max of 61440000 S/s (61.44 MS/s)
sdr.rx_lo =Fc #Carrier frequency of RX path (433.9 MHz)

#sdr.tx_lo = 2000000000
#sdr.tx_cyclic_buffer = True #sent data will keep getting repeated
#sdr.tx_hardwaregain_chan0 = -30

sdr.gain_control_mode_chan0 = "slow_attack" #Mode of receive path AGC(Automatic Gain Control). 
#Options are: slow_attack, fast_attack, manual
#slow_attack is for when the signal you are receiving has gradually changing power levels
#while fast_attack is for rapidly changing power levels


# Configuration of data channel
sdr.rx_enabled_channels = [0] #enable only one rx channel