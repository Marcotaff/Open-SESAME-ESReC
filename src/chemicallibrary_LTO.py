

from chemicallibrary import chemicallibrary
import pandas as pd
import numpy as np
import math


class chemicallibrary_LTO(chemicallibrary):
    
    def __init__(self):
        self.v_ref = np.array(pd.read_csv('LTO SoC-OCV.csv'))[:, 1]  # voltage values at different soc values from 0% to 100% SoC
        self.r_ref = np.array(pd.read_csv('r-soc-temp (extensive,1Hz).csv', header=None))
        
        self.vMax = self.v_ref[-1]
        self.vMin = self.v_ref[0]
        
       

        self.refCal = 0.0024/86400 #[%/s]
        self.refCyc = 0.002  # [%/EFC]
        
        self.refSor_cyc = 0.0001 # [%/EFC]
        self.refSor_cal= 0.0038/86400 #[%/s]
        
        
        self.Q=5
        
        
        self.max_Temp=45
        self.min_Temp=0
        
        self.maxSoC=1
        self.minSoC=0
        
        self.max_DOD=1
        
        self.max_Crate=5
        self.min_Crate=-5
        
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
        SoC=SoC
        
        #DoD check
        if DoD > self.max_DOD:
            DoD=self.max_DOD
            self.limitflag_DoD=1
        if DoD < 0:
            DoD=0
            self.limitflag_DoD=-1
        
        
        #Crate Check
        if Crate > self.max_Crate:
            Crate=self.max_Crate
            self.limitflag_Crate=1
        
        if Crate < self.min_Crate:
            Crate=self.min_Crate
            self.limitflag_Crate=-1
        
        return Temp,SoC,DoD,Crate



    def OCVfromSoC(self, SoC):
        
        #SoC 0-100
        
        SoC=SoC*100
        
        soc_ceil = math.ceil(SoC)
        soc_floor = math.floor(SoC)
        
        v_ceil=self.v_ref[soc_ceil]
        v_floor=self.v_ref[soc_floor]
        
        x=[soc_floor,soc_ceil]
        y=[v_floor, v_ceil]
        
        v_soc=np.interp(SoC,x,y)
        
        return v_soc

    def RfromTempSoC(self, SoC, temp):
        
       
        socConsider = math.ceil(SoC)
        tempConsider = temp - (-20)
        return self.r_ref[tempConsider, socConsider]

    
    #SoH Cal
    def Imp_CalSoC(self, SoC):
        #SoC 0-100
        SoC=SoC*100
        imp = 0.0866 * math.exp(0.0516*SoC)
        return imp
    

    def Imp_CalTemp(self, temp):
       
        imp = 0.0637 * math.exp(0.1002*temp)
        return imp

    #SoH Cyc
    def Imp_CycAvgSoc(self, asoc):
        
        imp=1
        return imp

    def Imp_CycTemp(self, temp):
        
        imp=0.275 * math.exp(0.041*temp) 
        return imp 


    def Imp_CycDod(self, DoD):
        
        DoD=DoD*100
        imp=0.03 *math.exp(0.032*DoD) 
        return imp

    def Imp_CycCrate(self, crate):
    
        #same function for both sides? +/-
        crate=abs(crate)
        imp = 0.0833*crate**2 - 0.4028*crate + 1.3194 
        return imp


    #SoR cyclic stressfactors 
    def Imp_SorAvgSoc(self, asoc):
        imp=1
        return imp

    def Imp_SorDoD(self, dod):
        imp=1
        return imp

    def Imp_SorCrate(self, crate):
        imp=1
        return imp
    
    def Imp_SorTemp(self,Temp):
        imp=1
        return imp
    

    #SoR cal stressfactors 
    def Imp_SorCalSoC(self,SoC):
        
        SoC=SoC*100
        imp=-0.0002*SoC**2 + 0.0237* SoC + 0.1661 
        return imp
   
    def Imp_SorCalTemp(self,Temp):
        imp=0.0006*math.exp(Temp*0.074)
        return imp
    
   





'''
class chemicallibrary_LTO(chemicallibrary):

    def __init__(self):
        self.v_ref = np.array(pd.read_csv('LTO SoC-OCV.csv'))[:, 1]  # voltage values at different soc values from 0% to 100% SoC
        self.r_ref = np.array(pd.read_csv('r-soc-temp (extensive,1Hz)LTO.csv', header=None))
        self.vMax = self.v_ref[-1]
        self.vMin = self.v_ref[0]
        self.refCal = 0.0024/86400 #In pers Seconds 
        self.refCyc = 0.002  #per full eq_cycle in percentage 
        self.refSor = 0.002 
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


    #Performance related Functions 
    def OCVfromSoC(self, soc): #ok
        socConsider = math.ceil(soc*100)
        return self.v_ref[socConsider]

    def RfromTempSoC(self, soc, temp): #ok 
        
        soc=100*soc

        temp_max=40
        temp_min=-20
        
        if temp> temp_max:
            temp=temp_max
            
        if temp<temp_min:
            temp=temp_min
        
        socConsider = math.ceil(soc)
        tempConsider = temp - (-20)
        
        print(tempConsider)
        print(socConsider)
        return self.r_ref[tempConsider, socConsider]
        
    #Calendaric Stressfactors SOH
    def Imp_CalSoC(self, soc): #ok
        soc=soc
        imp = 0.0866 * math.exp(0.0516*soc)
        return imp

    def Imp_CalTemp(self, temp):#ok
        
        temp_max=40
        temp_min=0
        
        if temp> temp_max:
            temp=temp_max
            
        if temp<temp_min:
            temp=temp_min
        
        imp = 0.0637 * math.exp(0.1*temp)
        return imp

    # Cyclic Stressfactors SOH 
    def Imp_CycAvgSoc(self, asoc):
        imp = 0.775 * asoc + 0.6025
        return imp

    
    def Imp_CycTemp(self, temp): #ok
        
        temp_max=45
        temp_min=0
        
        if temp> temp_max:
            temp=temp_max
            
        if temp<temp_min:
            temp=temp_min
        
        imp =0.275 * math.exp(0.041*temp)
        return imp


    def Imp_CycDod(self, dod): #ok
        dod=100*dod
        imp = 0.03 * math.exp(0.032*dod) 
        return imp


    def Imp_CycCrate(self, crate): #ok
        
        max_crate=10
        min_crate=-10
        
        if crate > max_crate:
            crate=max_crate
        
        if crate < min_crate:
            crate=min_crate
             
        imp=0.0833*crate**2 - 0.4028* crate + 1.3194  
          
        return imp
    
    #SoR Cyclic Stressfactors 
    def Imp_SorAvgSoc(self, asoc):
        
         
        imp = 13.28 * asoc ** 2 - 14.015 * asoc + 4.6873
        return imp

    def Imp_SorDoD(self, dod):
        dod=100*dod
        imp = 0.0742 * math.exp(0.026 * dod)
        return imp

    def Imp_SorCrate(self, crate):
        
        max_crate=2
        min_crate=-2
        
        if crate > max_crate:
            crate=max_crate
        
        if crate < min_crate:
            crate=min_crate
        

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
    
     #SoR Cal Stressfactors
'''


