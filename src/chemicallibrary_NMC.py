
from abc import ABCMeta, abstractmethod
import chemicallibrary 
import pandas as pd
import numpy as np
import math


class chemicallibrary_NMC(chemicallibrary.chemicallibrary):

    def __init__(self):
        self.v_ref = np.array(pd.read_csv('NMC SOC-OCV 2.csv'))[:, 1]  # voltage values at different soc values from 0% to 100% SoC
        self.r_ref = np.array(pd.read_csv('r-soc-temp (extensive,1Hz).csv', header=None))
        self.vMax = self.v_ref[-1]
        self.vMin = self.v_ref[0]
        self.refCal = 0.0149/86400 #In pers Seconds 
        self.refCyc = 0.0129  #per full eq_cycle
        self.refSor = 0.015 

    def OCVfromSoC(self, soc, v_ref):
        socConsider = math.ceil(soc)
        return v_ref[socConsider]

    def RfromTempSoC(self, soc, temp, r_ref):
        socConsider = math.ceil(soc)
        tempConsider = temp - (-20)
        return r_ref[tempConsider, socConsider]
        
    def Imp_CalSoC(self, soc):
        imp = 0.0077 * soc + 0.2525
        return imp

    def Imp_CalTemp(self, temp):
        imp = 0.0875 * np.exp(0.0556 * temp)
        return imp

    def Imp_CycAvgSoc(self, asoc):
        imp = 0.775 * asoc + 0.6025
        return imp

    def Imp_CycTemp(self, temp):
        imp = 0.0875 * math.exp(0.0556 * temp)
        return imp

    def SF_CycDod(self, dod):
        imp = 0.0002 * dod ** 2 - 0.0059 * dod + 0.9
        return imp

    def SF_CycCrate(self, cr):
        if cr > 0:  # charging
            imp = 0.0035 * math.exp(5.5465 * cr)
        else:  # discharging
            imp = 0.1112 * abs(cr) + 0.8219
            
        imp=1 #test !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        return imp

    def Imp_SorAvgSoc(self, asoc):
        imp = 13.28 * asoc ** 2 - 14.015 * asoc + 4.6873
        return imp

    def Imp_SorDoD(self, dod):
        imp = 0.0742 * math.exp(0.026 * dod)
        return imp

    def SF_SorCrate(self, cr):
        if cr > 0:  # charging
            imp = 0.19 * math.exp(5.0548 * cr)  # stress factor for charging c-rate (sor increase)
        else:  # discharging
            imp = 0.7986 * math.exp(0.5102 * abs(cr))
        return imp