

import numpy as np
import pandas as pd



#this class defines a simulation input object
class simulation_output():
    def __init__(self,Results):            
        
    
        
        self.Cylces_results=Results[0]
        self.deg_results=Results[1]
        self.pref_results=Results[2]
        
        self.Results=pd.DataFrame()
        
        #Get last SoH value
        self.SoH_end=self.pref_results.SoH.iloc[-1]
        self.SoR_end=self.pref_results.SoR.iloc[-1]
       

    #get data as pandas data frame with time vector as index
    def get_def_resultarray(self,start_SoH,start_SoR):    
        
        Results=np.zeros((len(self.deg_results),4))
        
        for i in range(0,len(self.deg_results)):
            
            if i ==0:
            
                Results[i,0]=start_SoH-self.deg_results.ToT_Cyc.iloc[i]/100 #SoH_cyc
                Results[i,1]=start_SoH-self.deg_results.Tot_Cal.iloc[i]/100 #SoH_cal
                Results[i,2]=start_SoH-self.deg_results.ToT_Cyc.iloc[i]/100-self.deg_results.Tot_Cal.iloc[i]/100 #Total SoH
                Results[i,3]=start_SoR+self.deg_results.Tot_SoR.iloc[i]/100
        
            else:
                Results[i,0]=Results[i-1,0]-self.deg_results.ToT_Cyc.iloc[i]/100 #SoH_cyc
                Results[i,1]=Results[i-1,1]-self.deg_results.Tot_Cal.iloc[i]/100 #SoH_cal
                Results[i,2]=Results[i-1,2]-self.deg_results.ToT_Cyc.iloc[i]/100-self.deg_results.Tot_Cal.iloc[i]/100 #Total SoH
                Results[i,3]=Results[i-1,3]+self.deg_results.Tot_SoR.iloc[i]/100
        
        columns = ['SoH_cyc','SoH_cal','Tot_SoH','SoR_Tot']    
        Results = pd.DataFrame( Results, columns = columns ) 
        
        self.Results=pd.DataFrame()
        
        self.Results["SoH_cyc"]=Results.SoH_cyc
        self.Results["SoH_cal"]=Results.SoH_cal
        self.Results["SoH_tot"]=Results.Tot_SoH
        self.Results["SoR_tot"]=Results.SoR_Tot
        self.Results["SoH_feedback"]=self.pref_results.SoH
        self.Results["SoR_feedback"]=self.pref_results.SoR
        self.Results["SoC"]=self.pref_results.SoC
        self.Results["Crate"]=self.pref_results.Crate
        self.Results["Power_sim_input"]=self.pref_results.power_sim_in
        self.Results["Power_updated"]=self.pref_results.power_upd
        self.Results["Bat_temp"]=self.pref_results.Bat_temp
        self.Results["Resistance"]=self.pref_results.Resistance
        self.Results["OCV_Voltage"]=self.pref_results.OCV_voltage
        self.Results["V_Bat"]=self.pref_results.V_Bat
        self.Results["limit_ChekV"]=self.pref_results.limChekV
        self.Results["limit_ChekSoC"]=self.pref_results.limCHeckSoC
        
        return self.Results
    
    
    def write_def_csv(self, filename, separator=','):
        
        self.Results.to_csv(filename, sep=separator)
        
        return
    
    
    
  
        
   



  
        
 
