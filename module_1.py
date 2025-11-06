import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import time
import adi
import json

num_seconds = 10
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
Fc = (int)(433.9e6) #carrier frequency
bandwidth = 200e3 #Bandwidth of front-end analog filter of RX path
Fm = bandwidth/2
Fs = (int)(521e3) #sampling frequency of ADC in samples per second
buffer_size = (int)(2 ** 12)

# Configure properties
sdr.rx_rf_bandwidth = (int)(bandwidth) #Bandwidth of front-end analog filter of RX path
                      #max of 20MHz for AD9363
                      #will we have to limit bandwidth further bc data limitations?

sdr.rx_sample_rate = Fs #Sample rate RX and TX paths in samples per second
                            #max of 61440000 S/s (61.44 MS/s)
sdr.rx_lo =(int)(Fc) #Carrier frequency of RX path (433.9 MHz)

#sdr.tx_lo = 2000000000
#sdr.tx_cyclic_buffer = True #sent data will keep getting repeated
#sdr.tx_hardwaregain_chan0 = -30

sdr.gain_control_mode_chan0 = "manual" #Mode of receive path AGC(Automatic Gain Control). 
#Options are: slow_attack, fast_attack, manual
#slow_attack is for when the signal you are receiving has gradually changing power levels
#while fast_attack is for rapidly changing power levels

sdr.rx_hardwaregain_chan0 = 50
#sdr gain 50


# Configuration of data channel unneeded
sdr.rx_enabled_channels = [0] #enable only one rx channel
sdr.rx_buffer_size =  buffer_size  #Size of receive buffer in samples
#too high

#final_data = [0] * ((int)(Fs * num_seconds))
#use numpy zeros, set datatype to complex
final_data = np.zeros(Fs * num_seconds + (buffer_size-(Fs*num_seconds)%buffer_size), dtype=complex)


#sdr_rx 4096 final data Fs *capture time 0-4096 4096-8112

def dataCapture() -> list:
    #This function begins the capture of data at given frequencies to decode the thermometers
    data = sdr.rx()
    Rx_0 = data
    return Rx_0



# ----------------------------------------------------------
# Define the handmade spectrogram function
def myspectrogram(data,N,M,Fs):
    
    # Calculate number of windows to be processed
    num_windows = int((len(data) - (M/2)) // (N - (M/2)))
    
    # Generate Hamming window
    hamming_window = np.hamming(N)

    # Define time instances for FFT slices
    t_spectro = np.arange(0, (num_windows)*(N*(1/Fs)), N*(1/Fs))

    # Define FFT bin frequencies (normalized by 2\pi)
    f_spectro = np.arange(0, 1, 1/N)

    # Divide up data into blocks of size N, with M/2 overlap with previous
    # block and M/2 overlap with next block, and multiple with hamming window
    spectrogram_results = np.zeros((num_windows,N))
    for i in range(num_windows):
        start_ind = i*(int(N - (M/2)))
        seg = data[start_ind:(start_ind + N)]
        windowed_seg = seg*hamming_window
        abs_fft_result = np.abs(np.fft.fft(windowed_seg))
        spectrogram_results[i] = abs_fft_result

    return t_spectro, f_spectro, spectrogram_results


def save_data(file_name, data):
    with open(file_name, 'w') as file:
        json.dump(data, file)

def retrieve_data(file_name):
    with open(file_name, 'r') as file:
        data = json.load(file)
        return data

def main():
    #data = dataCapture()
    #try:

        for start in range(0, num_seconds*Fs, buffer_size):
            print(x)
            end = start + buffer_size
            final_data[start:end] = sdr.rx()
            
            #for y in range((int)(Fs)): #dont need, directly copy 
                #print(y)
                #final_data[x*Fs + y] = data[y]
        print("i did da loops")
    #finally:
        #save_data('spectrogram.json', final_data)
        #t_spectro, f_spectro, specresults =  myspectrogram(final_data, 256, 64, Fs)
        #t_spectro1, f_spectro1, specresults1 = signal.spectrogram(final_data,Fs,'hamming',256,64)

        # ----------------------------------------------------------
        plt.specgram(final_data, Fs=Fs, NFFT=256, noverlap=64, Fc=Fc)
        # Plot handmade version of spectrogram using color mesh plotting routine
        #plt.pcolormesh(t_spectro,f_spectro,np.log10(specresults.T),shading='auto')
        #plt.ylabel('Frequency [Hz]')
        #plt.xlabel('Time [seconds]')
        plt.show()

main()