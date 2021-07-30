

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#this class defines a simulation input object
class simulation_output():
    def __init__(self,Results):            
        
    
        self.pref_results=Results[0]
        self.Cylces_results=Results[1]
        self.deg_results=Results[2]
      
        
        #Last_array
        Last_array=self.pref_results[-1]
        
        self.SoH_end=Last_array.SoH.iloc[-1]
        self.SoR_end=Last_array.SoR.iloc[-1]
       
        
    def SoC_plt(self):
        
        First=self.pref_results[0]
        
        
        middlearray=len(self.pref_results)
        middle_index=round(middlearray/2)
        
        Middle=self.pref_results[middle_index]
    
        Last=self.pref_results[-1]
        
        
    
        fig1, axs = plt.subplots()
        axs.plot(First.SoC,label="iteration 0")
        axs.plot(Middle.SoC,label="iteration "+str(middle_index))
        axs.plot(Last.SoC,label="iteration "+str(len(self.pref_results)))
        axs.set_ylabel('SoC')
        axs.grid(True)
        
        plt.legend()
        plt.show()
        
        
        
        
        return
    
    def iteration_results(self,start_SoH,start_SoR):
        
        length=len(self.pref_results)
        
        Results=np.zeros((length,7))
        
        
        
        for x in range(0,length):
            
            #Open Array 
            temp=self.pref_results[x]
            
            Results[x,0]=temp.SoH.iloc[-1]
            Results[x,1]=temp.SoR.iloc[-1]
            Results[x,6]=temp.calculation_iteration.iloc[-1]
            
            #Open another array 
            temp=self.deg_results[x]
        
            if x ==0:

                Results[x,2]=start_SoH-temp.SoH_ToT_Cyc.sum()/100 #SoH_cyc
                Results[x,3]=start_SoH-temp.SoH_ToT_Cal.sum()/100 #SoH_cal
                Results[x,4]=start_SoH-temp.SoH_ToT_Cal.sum()/100-temp.SoH_ToT_Cyc.sum()/100 #Total SoH
                Results[x,5]=start_SoR+temp.SoR_ToT_Cyc.sum()/100 #SoR
            
            else:
                
                Results[x,2]=Results[x-1,2]-temp.SoH_ToT_Cyc.sum()/100 #SoH_cyc
                Results[x,3]=Results[x-1,3]-temp.SoH_ToT_Cal.sum()/100 #SoH_cal
                Results[x,4]=Results[x-1,4]-temp.SoH_ToT_Cal.sum()/100-temp.SoH_ToT_Cyc.sum()/100 #Total SoH
                Results[x,5]=Results[x-1,5]+temp.SoR_ToT_Cyc.sum()/100 #SoR
                
        
        #Save as PD Dataframe 
        columns = ['SoH','SoR','SoH_cyc','SoH_cal','Tot_SoH','SoR_Tot','calculation_iteration']    
        Results = pd.DataFrame( Results, columns = columns )        
        
        line=np.zeros((2,2))
        
        line[0,0]=Results.calculation_iteration.iloc[0]
        line[0,1]=Results.SoH.iloc[0]
        
        line[1,0]=Results.calculation_iteration.iloc[-1]
        line[1,1]=Results.SoH.iloc[-1]
        
        temp=self.pref_results[2]
        
        a=temp.calculation_iteration.iloc[-1]
        b=temp.SoH.iloc[-1]
        
        deltaT=a-Results.calculation_iteration.iloc[0]
        deltaSoH=Results.SoH.iloc[0]-b
        
        m=-deltaSoH/deltaT
        c=b-m*a
        Results["new_line"]=""
    
        for x in range(0,len(Results)):
            Results.new_line.iloc[x]=Results.calculation_iteration.iloc[x]*m+c
        
        
        delta=Results.new_line.iloc[-1]-Results.SoH.iloc[-1]
       
        '''
        fig2, axs = plt.subplots()
        axs.scatter(Results.calculation_iteration,Results.SoH,label="SoH_Sim")
        axs.plot(line[:,0],line[:,1])
        axs.plot(Results.calculation_iteration,Results.new_line,label="SoH_lin_extrapoliert")
        axs.set_ylabel('SoH')
        axs.grid(True)
        axs.set_ylabel('SoH')
        axs.set_xlabel('Number of Iterations')
        axs.set_title('SOH calc deviation '+str(round(delta*100,2))+'%SoH')
        plt.legend()
        plt.show()
        '''
        
        
        
        
        return Results
        
        
        

    '''
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
   '''
    
    
  
        
   



  
        
 
