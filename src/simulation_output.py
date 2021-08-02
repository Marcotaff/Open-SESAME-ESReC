

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
        
        First_iteration=First.calculation_iteration.loc[0]
        Last_iteration=Last.calculation_iteration.loc[0]
        Middle_iteration=Middle.calculation_iteration.loc[0]
    
    
    
        fig1, axs = plt.subplots()
        
        string="iteration:"+str(First_iteration)
        axs.plot(First.SoC,label=string)
        
        string="iteration:"+str(Middle_iteration)
        axs.plot(Middle.SoC,label=string)
        
        string="iteration:"+str(Last_iteration)
        axs.plot(Last.SoC,label=string)
        axs.set_ylabel('SoC')
        axs.set_xlabel('timestep')
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
            
            if x==0:
                delta_iteration=1
            else:   
                delta_iteration=Results[x,6]-Results[x-1,6]
            #Open another array 
            temp=self.deg_results[x]
        
        
            if x ==0:

                Results[x,2]=start_SoH-temp.SoH_ToT_Cyc.sum()/100 #SoH_cyc
                Results[x,3]=start_SoH-temp.SoH_ToT_Cal.sum()/100 #SoH_cal
                Results[x,4]=start_SoH-temp.SoH_ToT_Cal.sum()/100-temp.SoH_ToT_Cyc.sum()/100 #Total SoH
                
                
                
                Results[x,5]=start_SoR+temp.SoR_ToT_Cyc.sum()/100 #SoR
            
            else:
                
                Results[x,2]=Results[x-1,2]-(temp.SoH_ToT_Cyc.sum()/100)* delta_iteration #SoH_cyc
                Results[x,3]=Results[x-1,3]-(temp.SoH_ToT_Cal.sum()/100 )*delta_iteration#SoH_cal
                Results[x,4]=Results[x-1,4]-(temp.SoH_ToT_Cal.sum()/100-temp.SoH_ToT_Cyc.sum()/100)* delta_iteration #Total SoH
                
                
                
                Results[x,5]=Results[x-1,5]+(temp.SoR_ToT_Cyc.sum()/100)*delta_iteration#SoR
                
        
        #Save as PD Dataframe 
        columns = ['SoH','SoR','SoH_cyc','SoH_cal','Tot_SoH','SoR_Tot','calculation_iteration']    
        Results = pd.DataFrame( Results, columns = columns )        
        
       
        
        return Results
        
        
    def SoH_plt(self,Results):
        
        
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
        
        
        return 
        
        
        




  
        
 
