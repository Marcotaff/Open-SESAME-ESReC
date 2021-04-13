import numpy as np
from numpy import exp
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
        
    soc_prof[0]=soc1
    soc_prof[-1]=soc2
        
    return sf_cyc,sf_sor

