from chemicallibrary import chemicallibrary
import pandas as pd
import numpy as np
import math


class chemicallibrary_NMC(chemicallibrary):

    def __init__(self):
        
        self.v_ref = np.array(pd.read_csv('NMC SOC-OCV 2.csv'))[:, 1]  # voltage values at different soc values from 0% to 100% SoC
        self.r_ref = np.array(pd.read_csv('r-soc-temp (extensive,1Hz).csv', header=None))
        self.vMax = self.v_ref[-1]
        self.vMin = self.v_ref[0]
        self.refCal = 0.0149/86400 #In pers Seconds 
        self.refCyc = 0.0129  #per full eq_cycle in percentage 
        
        self.refSor_cyc = 0.015 
        self.refSor_cal=0
        
        
        self.Q=5
        
        
        self.max_Temp=40
        self.min_Temp=0
        
        self.maxSoC=1
        self.minSoC=0
        
        self.max_DOD=1
        
        self.max_Crate=2
        self.min_Crate=-2
        
        self.limitflag_temp=0
        self.limitflag_SoC=0
        self.limitflag_DoD=0
        self.limitflag_Crate=0
        
        
        
    def operational_range_check(self,Temp,SoC,DoD,Crate):
        
        #Temp check
        if Temp > self.max_Temp:
            Temp=self.max_Temp
            self.limitflag_temp=1
              
        if Temp<self.min_Temp:
            Temp=self.min_Temp
            self.limitflag_temp=-1
        
        #SoC check
        if SoC > self.maxSoC:
            SoC=self.maxSoC
            self.limitflag_SoC=1
        if SoC < self.minSoC:
            SoC=self.minSoC=0
            self.limitflag_SoC=-1
        SoC=SoC*100
        
        #DoD check
        if DoD > self.max_DOD:
            DoD=self.max_DOD
            self.limitflag_DoD=1
        if DoD < 0:
            DoD=0
            self.limitflag_DoD=-1
        DoD=100*DoD
        
        #Crate Check
        if Crate > self.max_Crate:
            Crate=self.max_Crate
            self.limitflag_Crate=1
        
        if Crate < self.min_Crate:
            Crate=self.min_Crate
            self.limitflag_Crate=-1
        
        return Temp,SoC,DoD,Crate



    def OCVfromSoC(self, SoC):
        
        #SoC Check 
    
        socConsider = math.ceil(SoC*100)
        return self.v_ref[socConsider]

    def RfromTempSoC(self, SoC, temp):
        
       
        socConsider = math.ceil(SoC)
        tempConsider = temp - (-20)
        return self.r_ref[tempConsider, socConsider]
        
    
    #SoH Cal
    def Imp_CalSoC(self, soc):
       
        imp = 0.0077 * soc + 0.2525  #SoC 0..100 ?
        return imp

    def Imp_CalTemp(self, temp):
        
        imp = 0.0875 * np.exp(0.0556 * temp)
        return imp

    #SoH Cyc
    def Imp_CycAvgSoc(self, asoc):
        asoc=asoc/100
        imp = 0.775 * asoc + 0.6025
        return imp

    
    def Imp_CycTemp(self, temp):
        
        imp = 0.0008*temp**2 - 0.033*temp + 0.8349
        return imp


    def Imp_CycDod(self, dod):
       
        imp = 0.0001 * dod ** 2 - 0.0044 * dod + 0.9
        return imp

    def Imp_CycCrate(self, crate):
        
             
        if crate > 0:  # charging
            imp = 0.0035 * math.exp(5.5465 * crate)
        else:  # discharging
            imp = 0.1112 * abs(crate) + 0.8219
        return imp



    #SoR cyclic stressfactors 
    def Imp_SorAvgSoc(self, asoc):
        #SoC 0-100
        
        asoc=asoc/100
        imp = 13.28 * asoc ** 2 - 14.015 * asoc + 4.6873  
        return imp

    def Imp_SorDoD(self, dod):
        #DoD 0-100
        
        imp = 0.0742 * math.exp(0.026 * dod)
        return imp

    def Imp_SorCrate(self, crate):
        
        if crate > 0:  # charging
            imp = 0.19 * math.exp(5.0548 * crate)  # stress factor for charging c-rate (sor increase)
        else:  # discharging
            imp = 0.7986 * math.exp(0.5102 * abs(crate))
        
        return imp
    
    def Imp_SorTemp(self,Temp):
        
        
        imp=1 #Temp
        
        return imp
    
    
    
    #SoR cal stressfactors 
    def Imp_SorCalSoC(self,SoC):
        
        imp=1
        
        return imp
    
    
    def Imp_SorCalTemp(self,Temp):
        
        imp=1
        
        return imp 
    
    
    
    
    
    
    
    
    
