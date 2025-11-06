import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import time
import adi
import json

Fc = (int)(433.9e6) #carrier frequency
bandwidth = 10e6 #Bandwidth of front-end analog filter of RX path
Fs = (int)(521e3) #sampling frequency of ADC in samples per second
buffer_size = (int)(2 ** 12)

samples = np.load('samples.npy') #load saved data

plt.specgram(samples, Fs=Fs, NFFT=256, noverlap=64, Fc=Fc)
#plt.savefig('plot.png')
plt.show()
print("image made")
