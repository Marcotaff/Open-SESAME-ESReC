# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 14:58:40 2021

@author: blm8
"""

import pandas as pd
import math
from cell import Cell
from degradation_analysis import degradation
import numpy as np




def simulation(data,input_parameter):
    
    #_______________________________________________________________________________________________
    # Building Class Objects 
    
    #Cell obj
    Cell_Obj=Cell(input_parameter.initial_SoC,input_parameter.initial_Temp,input_parameter.initial_SoR,input_parameter.initial_SoH,input_parameter.nominal_energy,input_parameter.lim_Mode,input_parameter.initial_Q)      

    #Degradation obj
    Bat_deg= degradation(input_parameter.Cell_chemistry,input_parameter.timeresolution)
    
    #_______________________________________________________________________________________________
    #predefine output arrays
    
    Cyc_results=pd.DataFrame()
    deg_results=pd.DataFrame()
    
    #_______________________________________________________________________________________________
    #Repetition handler  

    if input_parameter.repetition != 0:
    
        for i in range(0,input_parameter.repetition):
            
            if i == 0:
                
                power_W_temp=data.power_W
                temperature_C_temp=data.ambient_temperature_C
                
            else:
                power_W_temp=np.concatenate((power_W_temp,data.power_W),axis=0)
                temperature_C_temp=np.concatenate((temperature_C_temp,data.ambient_temperature_C),axis=0)
        
        data.power_W=power_W_temp
        data.ambient_temperature_C=temperature_C_temp
     
    #_______________________________________________________________________________________________
    # define amount of fractions  
    
    inputdata_len=len(data.power_W)
    amount_fractions=math.ceil(inputdata_len/input_parameter.fraction_size)

    start_index=1
    
    #_______________________________________________________________________________________________
    # Looping threw fractions 
    
    for i in range(1,int(amount_fractions)+1):
        
        end_index=start_index+input_parameter.fraction_size-1
            
        #Check if end_index in range of input_data
        if end_index > inputdata_len:
                end_index=inputdata_len
            
            
        #select straight from numpy input data
        fraction_power = data.power_W[start_index:end_index]
        fraction_Tambient = data.ambient_temperature_C[start_index:end_index]
            
        start_index=end_index+1
        
  
        #_______________________________________________________________________________________________
        #Performance Analysis
        temp_results_np=np.zeros((len(fraction_power),8)) #Create temperorary result array
        
        for x in range(0,len(fraction_power)):
        
            #power=fraction_data.power.to_numpy()
            #temperature=fraction_data.temperature.to_numpy()
    
            bat_temp=fraction_Tambient[x] # ambient temp == bat temp 
    
            #Get circuit parameters 
            #r_ref=1 #??????????????????????
            Resistance=1#Bat_deg.Chemistry_obj.RfromTempSoC(Cell_Obj.SoC,bat_temp,r_ref)
            OCVoltage=Bat_deg.Chemistry_obj.OCVfromSoC(Cell_Obj.SoC) #SoC value of the timestep before 
            Vmax=Bat_deg.Chemistry_obj.vMax
            Vmin=Bat_deg.Chemistry_obj.vMin
        
            Cell_Obj.CheckV(Resistance,fraction_power[x],OCVoltage,Vmax,Vmin)
            Cell_Obj.CalSoC(fraction_power[x],input_parameter.timeresolution,input_parameter.SoC_max,input_parameter.SoC_min)
            
            
            #save results of fracment
            temp_results_np[x]=[Cell_Obj.SoC,Cell_Obj.Crate,OCVoltage,Cell_Obj.Vinst,Cell_Obj.updated_current,Resistance,Cell_Obj.limCheckV,Cell_Obj.limCheckSoC]
            
        temp_results = pd.DataFrame(temp_results_np, columns = ['Cell_Obj.SoC','Cell_Obj.Crate','OCV_voltage','V_Bat','I_Updated','Resistance','limChekV','limCHeckSoC'])
        
        
        #_______________________________________________________________________________________________
        #degradation Analysis
    
        Cyc_results_temp,deg_results_temp =Bat_deg.compute(temp_results_np[:,0],temp_results_np[:,1],fraction_Tambient[:],start_index)
        
        #_______________________________________________________________________________________________
        #Update SoH and SoR 
    
        Cell_Obj.update(Bat_deg.delta_SoH/100,Bat_deg.delta_SoR/100)
        
        print(Cell_Obj.SoH)
    
        #_______________________________________________________________________________________________
        #Save Results 
    
        #Save results i arrays 
        Cyc_results=pd.concat([Cyc_results,Cyc_results_temp])
        deg_results=pd.concat([deg_results,deg_results_temp])
    
     
    
    return Cyc_results,deg_results
  



