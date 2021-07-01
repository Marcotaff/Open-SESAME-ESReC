import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from numpy import exp
from math import ceil
from scipy.signal import find_peaks as fp

def ref_NMC():
    ref_cal = 0.0149/86400      # Reference degradation rate for calendar aging (%/s)
    ref_cyc = 0.01              # Reference degradation rate for cycle aging (%/fec)
    ref_sor = 0.015             # Reference increase in SoR (%/fec)
    return ref_cal,ref_cyc,ref_sor

def SF_tempcal_NMC(temp):
    sf = 0.0875 * exp(0.0556*temp)
    return sf

def SF_soccal_NMC(soc):
    sf = 0.0077*soc + 0.2525
    return sf

def SF_cyc_NMC(temp,soc_prof):
    soc1=soc_prof[0]       # hack to avoid the last points not being counted
    soc2=soc_prof[-1]
    soc_prof[-1]=0
    soc_prof[0]=1                  
    y=-1*soc_prof
    valleys = fp(y)[0]
    peaks = fp(soc_prof)[0]
    a=np.hstack((valleys,peaks))
    a.sort()
    sf_temp = 0.0008*temp**2 - 0.033*temp + 0.8349
    sf_cyc = 0
    sf_sor = 0
    
    for i in range(len(a)-1):
        dod = abs(soc_prof[a[i]]-soc_prof[a[i+1]])*100                # dod computation for cycle aging
        fec = dod/2/100                                               # full equivalent cycles in current step
        cr = (soc_prof[a[i+1]]-soc_prof[a[i]])/((a[i+1]-a[i])/3600)   # c-rate in current step
        msoc = (soc_prof[a[i]]+soc_prof[a[i+1]])/2                    # mean soc in current step
        
        if cr>0:        # charging
            sf_cr = 0.0035 * exp(5.5465*cr)                     # stress factor for charging c-rate (cycle aging)
            sf_cr_sor = 0.19 * exp(5.0548*cr)                   # stress factor for charging c-rate (sor increase)
        else:           # discharging
            sf_cr = 0.1112*abs(cr) + 0.8219                     # stress factor for discharging c-rate (cycle aging)
            sf_cr_sor = 0.7986*exp(0.5102*abs(cr))              # stress factor for discharging c-rate (sor increase)
                        
        sf_dod = 0.0001*dod**2 - 0.0044*dod + 0.9               # stress factor for dod (cycle aging)
        sf_dod_sor = 0.0742*exp(0.026*dod)                      # stress factor for dod (sor increase)
            
        sf_soc = 0.74*msoc + 0.6008                             # stress factor for mean soc (cycle aging)
        sf_soc_sor = 13.28*msoc**2 - 14.015*msoc + 4.6873       # stress factor for mean soc (sor increase)
        
        sf_cyc+= sf_cr * sf_dod * sf_temp * sf_soc * fec
        sf_sor+= sf_cr_sor * sf_dod_sor * sf_soc_sor * fec
        
    soc_g[0]=soc1
    soc_g[-1]=soc2
        
    return sf_cyc,sf_sor


# READING FILES FOR INPUT
ip = np.array(pd.read_excel(r'input_parameters.xlsx'))
input_profile = np.array(pd.read_csv('input.csv',header=None).values)     # CSV with power for every second of every day of the year/years (each second of the day in a new row, each day in a new column)
temp = np.array(pd.read_csv('geneva temp data.csv').values)       # CSV file containing daily average temperature data for a whole year in Geneva (in °C)

# FOLDER CREATION TO SAVE DAILY INPUT PROFILES AND FINAL RESULTS
fil_name = ip[7,1]                      # name to the file to which the daily input profiles will be stored
dir_name = os.getcwd()
os.mkdir(dir_name+'\\'+fil_name)        # making folder to save the figures
n = dir_name + '\\' + fil_name + '\\'

# '+' means power from the battery and '-' means power to the battery

# SCENARIO PARAMETERS
days = ip[6,1] # number of days you want to simulate
bsize = ip[0,1]                      # size of the battery in the vehicle (kWh)

# CELL PARAMETERS
Q0 = 1.5                    # cell capacity in Ah
soc_min = ip[1,1]           # minimum soc during cycling
soc_max = ip[2,1]           # maximum soc during cycling
v_max = ip[4,1]             # maximum voltage during cycling
v_min = ip[3,1]             # minimum voltage during cycling
soc = soc_in = ip[5,1]      # minimum initial SoC

# INITIALISATIONS
crate1 = np.zeros(86400)        # array to store c-rate profile actually followed by battery
Qcal = 0                        # cumulative calendar aging
Qcyc = 0                        # cumulative cycle aging
Qlcal = np.zeros(days+1)        # cumulative calendar aging array
Qlcyc = np.zeros(days+1)        # cumulative cycle aging array
Qlsor = np.ones(days+1)*100     # cumulative sor increase array
Q_soc_max = np.zeros(days)      # array for maximum SoC value each day
Q_soc_min = np.zeros(days)      # array for minimum SoC value each day
sor = 100                       # initial SoR value
Q = Q0                          # variable to be updated to account for capacity loss
soc_g = np.zeros(86400)         # array to record SoC values throughout the day
tfec = 0                        # total full equivalent cycles performed
prof = np.zeros(86400)          # array to hold the c-rate at every second of the day

# SOC-OCV CURVE AND RESISTANCE-TEMP-SOC MAP FOR NMC CELL
v_ref = np.array(pd.read_csv('NMC SOC-OCV 2.csv'))[:,1]                         # voltage values at different soc values from 0% to 100% SoC
r_ref=np.array(pd.read_csv('r-soc-temp (extensive,1Hz).csv', header=None))      # resistance matrix at different temperatures (-20°C to 40°C) and SoC (0% to 100%)

# PROFILE AND MODEL IMPLEMENTATION
ref_cal,ref_cyc,ref_sor = ref_NMC()             # setting the reference values for the desired battery chemistry

for j in range(days):
    
    temp1 = round(temp[j,0])                    # setting temperature for current day
    prof[:] = input_profile[:,j]/bsize          # convert power profile to c-rate profile and copy to another array
    t1 = 1 / 3600                               # converting seconds to hours (required by model)
    sf_tempcal = SF_tempcal_NMC(temp1)          # calculating stress factor for temperature (calendar aging) for the desired chemistry
    
    
    # CALENDAR AGING CALCULATIONS AND SOC UPDATE
    for i in range(len(prof)):
        
        unabs_c = prof[i]                               # c-rate value
        abs_c = abs(unabs_c)                            # absolute value of c-rate
        soc_g[i] = soc                                  # storing present soc to soc array
        soc_lookup = ceil(soc * 100)                    # soc for lookup in soc table (for ocv-soc curve and r-temp-soc map)
        sf_soccal = SF_soccal_NMC(soc_lookup)           # calendar aging SoC stress factor calculation
        Qtcal = ref_cal * sf_soccal * sf_tempcal        # total degradation in this 1 second timestep
        Qcal = Qcal + Qtcal                             # adding degradation in this time step to cumulative calendar aging
        
        soc = soc - unabs_c / (Q/Q0) * t1               # calculating new soc
        
        v = v_ref[soc_lookup] - unabs_c * Q0 * r_ref[temp1-(-20),soc_lookup] * sor/100      # calculating instantaneous voltage
        if soc>soc_max or soc<soc_min or v>v_max or v<v_min:
            soc = soc + unabs_c / (Q/Q0) * t1           # undo soc increase if voltage/soc limitations are crossed
            crate1[i] = 0
            Qtcyc = 0
        else:
            crate1[i] = unabs_c / (Q/Q0)
                
    # CYCLE AGING AND SOR INCREASE CALCULATIONS
    sf_cyc,sf_sor = SF_cyc_NMC(temp1,soc_g)
    Qcyc+=ref_cyc * sf_cyc             # adding cycle aging in current step to cumulative cycle aging
    sor+= ref_sor * sf_sor             # adding sor increase in current step to cumulative sor increase
        
    Qlcal[j+1] = Qcal                       # storing cumulative calendar aging at each time step for plotting later
    Qlcyc[j+1] = Qcyc                       # storing cumulative cycle aging at each step for plotting later
    Qlsor[j+1] = sor                        # storing cumulative sor increase at each step for plotting later
    Q = (1 - (Qcal + Qcyc) / 100) * Q0      # updating SoH
    Q_soc_max[j] = max(soc_g)               # storing maximum SoC in this day (for debugging purposes)
    Q_soc_min[j] = min(soc_g)               # storing minimum SoC in this day (for debugging purposes)
    
    
    name = str(j+1)
    name = n + name + '.png'
    plt.plot(prof,'r',crate1,'b',soc_g,'g'); plt.xlabel('time (s)'); plt.ylabel('C-rate / SoC'); plt.legend(['proposed','actual','SoC']); plt.savefig(name); plt.close()

plt.plot(Qlcal,'r',Qlcyc,'b',Qlcyc+Qlcal,'g')
plt.xlabel('time (days)'); plt.ylabel('Degradation (%)'); plt.legend(['calendar','cycle','total']); plt.savefig(n+'Degradation');
plt.close()
plt.plot(Qlsor)
plt.xlabel('time (days)'); plt.ylabel('SoR (%)'); plt.savefig(n+'SoR');
plt.close()
plt.plot(Q_soc_max,'r',Q_soc_min,'b')
plt.xlabel('time (days)'); plt.ylabel('SoC'); plt.legend(['SoC max','SoC min']); plt.savefig(n+'SoC range');
plt.close()

print('The calendar and cycle aging are '+ str(Qcal) + ' and ' + str(Qcyc) + ' respectively')
print('The SoR is ' + str(sor))