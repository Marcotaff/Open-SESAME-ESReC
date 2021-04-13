import numpy as np
import pandas as pd
import NMC
import matplotlib.pyplot as plt
from math import ceil

def deg_calc(cell_chem,bsize,v_min,v_max,soc_min,soc_max,soc_in,days,n,temp,input_profile):
    # INITIALISATIONS
    Q0 = 1
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
    prof = np.zeros(86400)          # array to hold the c-rate at every second of the day
    soc = soc_in
    
    if cell_chem == 'NMC':
        # SOC-OCV CURVE AND RESISTANCE-TEMP-SOC MAP FOR NMC CELL
        v_ref = np.array(pd.read_csv('NMC SOC-OCV 2.csv'))[:,1]                         # voltage values at different soc values from 0% to 100% SoC
        r_ref=np.array(pd.read_csv('r-soc-temp (extensive,1Hz).csv', header=None))      # resistance matrix at different temperatures (-20°C to 40°C) and SoC (0% to 100%)
        
        # PROFILE AND MODEL IMPLEMENTATION
        ref_cal,ref_cyc,ref_sor = NMC.ref_NMC()             # setting the reference values for the desired battery chemistry
        
        for j in range(days):
            
            temp1 = round(temp[j,0])                    # setting temperature for current day
            prof[:] = input_profile[:,j]/bsize          # convert power profile to c-rate profile and copy to another array
            t1 = 1 / 3600                               # converting seconds to hours (required by model)
            sf_tempcal = NMC.SF_tempcal_NMC(temp1)          # calculating stress factor for temperature (calendar aging) for the desired chemistry
            
            
            # CALENDAR AGING CALCULATIONS AND SOC UPDATE
            for i in range(len(prof)):
                
                unabs_c = prof[i]                               # c-rate value
                soc_g[i] = soc                                  # storing present soc to soc array
                soc_lookup = ceil(soc * 100)                    # soc for lookup in soc table (for ocv-soc curve and r-temp-soc map)
                sf_soccal = NMC.SF_soccal_NMC(soc_lookup)       # calendar aging SoC stress factor calculation
                Qtcal = ref_cal * sf_soccal * sf_tempcal        # total degradation in this 1 second timestep
                Qcal = Qcal + Qtcal                             # adding degradation in this time step to cumulative calendar aging
                
                soc = soc - unabs_c / (Q/Q0) * t1               # calculating new soc
                
                v = v_ref[soc_lookup] - unabs_c * Q0 * r_ref[temp1-(-20),soc_lookup] * sor/100      # calculating instantaneous voltage
                if soc>soc_max or soc<soc_min or v>v_max or v<v_min:
                    soc = soc + unabs_c / (Q/Q0) * t1           # undo soc increase if voltage/soc limitations are crossed
                    crate1[i] = 0
                else:
                    crate1[i] = unabs_c / (Q/Q0)
                        
            # CYCLE AGING AND SOR INCREASE CALCULATIONS
            sf_cyc,sf_sor = NMC.SF_cyc_NMC(temp1,soc_g)
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
            
    # if cell_chem == 'LTO':
        # fill in required code
    
    return Qlcal, Qlcyc, Qlsor, Q_soc_max, Q_soc_min