# ----------------------------------------------------------
# hello world for pluto based on ADI blog post
#
# 
# 10-29-2025
# ----------------------------------------------------------

# Copyright (C) 2022 Analog Devices, Inc.
#
# SPDX short identifier: ADIBSD

import time

import adi
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

# Create radio
sdr = adi.ad9361(uri="ip:192.168.2.1") #default pluto ip address is 192.168.2.1

# Configure properties
sdr.rx_rf_bandwidth = 4000000
sdr.sample_rate = 6000000
sdr.rx_lo = 2000000000
sdr.tx_lo = 2000000000
sdr.tx_cyclic_buffer = True #sent data will keep getting repeated
sdr.tx_hardwaregain_chan0 = -30
sdr.gain_control_mode_chan0 = "slow_attack"

# Configuration data channels
sdr.rx_enabled_channels = [0,1] #enable both rx channels
sdr.tx_enabled_channels = [0]

# Read properties
print("RX LO %s" % (sdr.rx_lo))

# Create a sinewave waveform
# Final result is a simple IQ data array 
fs = int(sdr.sample_rate)
N = 1024
fc = int(1000000 / (fs / N)) * (fs / N)
ts = 1 / float(fs)
t = np.arange(0, N * ts, ts)
i = np.cos(2 * np.pi * t * fc) * 2 ** 14
q = np.sin(2 * np.pi * t * fc) * 2 ** 14
iq = i + 1j * q

# Send data
sdr.tx(iq)

# Collect data
for r in range(20):
    data = sdr.rx() #collect the data from Pluto
    Rx_0 = data[0] 
    Rx_1 = data[1] 
    f, Pxx_den = signal.periodogram(Rx_0, fs)
    plt.clf()
    plt.semilogy(f, Pxx_den)
    plt.ylim([1e-7, 1e2])
    plt.xlabel("frequency [Hz]")
    plt.ylabel("PSD [V**2/Hz]")
    plt.draw()
    plt.pause(0.05)
    time.sleep(0.1)

plt.show()