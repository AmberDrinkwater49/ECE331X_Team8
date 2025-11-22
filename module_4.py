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