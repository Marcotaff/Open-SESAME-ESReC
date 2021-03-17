import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

# soc ocv curve for NMC cell
s = np.array(pd.read_csv('Sample GITT.csv').values)         # reading a CSV file with 3 columns (voltage [V], current [mA] and capacity [mAh])
v1 = np.zeros(1000)                                         # voltage progression while discharging
cap1 = np.zeros(1000)                                       # capacity progression while discharging
v2 = np.zeros(1000)                                         # voltage progression while charging
cap2 = np.zeros(1000)                                       # capacity progression while charging
k = 0
l = 1

# COPYING THE VOLTAGE AND CAPACITY WHILE CHARGING AND DISCHARGING IN DIFFERENT ARRAYS
for i in range(len(s)):
    if s[i,1]==0 and s[i+1,1]<0:
        v1[k]=s[i,0]
        cap1[k]=s[i,2]
        k=k+1
    elif s[i,1]==0 and s[i+1,1]>0:
        v1[k]=s[i,0]
        cap1[k]=s[i,2]
        k=k+1
        break

for j in range(i+1,len(s)):
    if s[j,1]==0 and s[j+1,1]>0:
        v2[l]=s[j,0]
        cap2[l]=s[j,2]
        l=l+1
        
volt1 = v1[0:k]                 # voltage progression during discharging
cap1 = cap1[0:k]                # capacity progression during discharging
volt2 = v2[0:l]                 # voltage progression during charging
volt2[0] = volt1[-1]            # voltage at end of discharging = voltage at start of charging
cap2 = cap2[0:k]                # capacity progression during charging
cap1 = (1-cap1/cap1[-1])        # converting capacity to SoC
cap2 = cap2/cap2[-1]            # converting capacity to SoC

volt2 = volt2[::-1]             # reversing progression in charging array to match discharge array
cap2 = cap2[::-1]               # reversing progression in charging array to match discharge array
f = interp1d(cap2,volt2)        # interpolation function for voltage and capacity values during charging
volt2new = f(cap1)              # charging voltage values for discharge capacity values
v_avg = (volt1+volt2new)/2      # finding the average voltage values (during charge and discharge)
f = interp1d(cap1,v_avg)        # function to interpolate and find ocv from soc, soc in fraction (between 0 and 1) and voltage in V

k=0
j=0

# BUILDING VOLTAGE LOOKUP TABLE
v_ref = np.zeros(101)           # voltage values for SoC from 0 to 1 in 0.01 steps
for i in range(100):
    v_ref[k] = f(j)
    k=k+1
    j=j+0.01
v_ref[k] = f(1)