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
    
    #Degradation obj
    Bat_deg= degradation(input_parameter.Cell_chemistry,input_parameter.timeresolution,input_parameter.cyc_count_alg)
     
    #Cell 
    initial_Bat_temp=data.ambient_temperature_C[0] 
    Cell_Obj=Cell(input_parameter.initial_SoC,initial_Bat_temp,input_parameter.initial_SoR,input_parameter.initial_SoH,input_parameter.nominal_energy,input_parameter.lim_Mode,Bat_deg.Chemistry_obj.Q)

    #_______________________________________________________________________________________________
    #predefine output arrays
    
    Cyc_results=pd.DataFrame()
    deg_results=pd.DataFrame()
    performance_results=pd.DataFrame()

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
    start_index=0
    
    #_______________________________________________________________________________________________
    # Looping threw fractions 
   
    
    for i in range(0,int(amount_fractions)):
        
        end_index=start_index+input_parameter.fraction_size
            
        #Check if end_index in range of input_data
        if end_index >= inputdata_len:
                end_index=inputdata_len
                 
        #select straight from numpy input data
        fraction_power = data.power_W[start_index:end_index]
        fraction_Tambient = data.ambient_temperature_C[start_index:end_index]
  
        index_cyc= start_index
        start_index=end_index
  
        #_______________________________________________________________________________________________
        #Performance Analysis
        temp_results_np=np.zeros((len(fraction_power),13)) #Create temperorary result array
        
        for x in range(0,len(fraction_power)):
        
            #Temperature Model
            bat_temp=fraction_Tambient[x] # ambient temp == bat temp 
            
            #Get circuit parameters 
            
            
            #print("SoH",Cell_Obj.SoH)
            
            Resistance=Bat_deg.Chemistry_obj.RfromTempSoC(Cell_Obj.SoC,bat_temp)
            OCVoltage=Bat_deg.Chemistry_obj.OCVfromSoC(Cell_Obj.SoC) #SoC value of the timestep before 
            Vmax=Bat_deg.Chemistry_obj.vMax
            Vmin=Bat_deg.Chemistry_obj.vMin
        
            #Check Voltage and SoC limits
            Cell_Obj.CheckV(Resistance,fraction_power[x],OCVoltage,Vmax,Vmin)
            Cell_Obj.CalSoC(Cell_Obj.Power_upd,input_parameter.timeresolution,input_parameter.SoC_max,input_parameter.SoC_min)
            
            #save results of fragment
            temp_results_np[x]=[Cell_Obj.SoR,Cell_Obj.SoH,Cell_Obj.SoC,Cell_Obj.Crate,Cell_Obj.Power_upd,OCVoltage,Cell_Obj.Vinst,Cell_Obj.updated_current,Resistance,Cell_Obj.limCheckV,Cell_Obj.limCheckSoC,bat_temp,fraction_power[x]]
            
            
        temp_results = pd.DataFrame(temp_results_np, columns = ['SoR','SoH','SoC','Crate','power_upd','OCV_voltage','V_Bat','I_Updated','Resistance','limChekV','limCHeckSoC','Bat_temp','power_sim_in'])
        
        #_______________________________________________________________________________________________
        #degradation Analysis
      
        Cyc_results_temp,deg_results_temp =Bat_deg.compute(temp_results_np[:,2],temp_results_np[:,3],fraction_Tambient[:],index_cyc)
        #_______________________________________________________________________________________________
        #Update SoH and SoR 
    
        Cell_Obj.update(Bat_deg.delta_SoH/100,Bat_deg.delta_SoR/100)
    
        
    
        #_______________________________________________________________________________________________
        #Save Results 
    
        #Save results i arrays 
        Cyc_results=pd.concat([Cyc_results,Cyc_results_temp],ignore_index=True)
        deg_results=pd.concat([deg_results,deg_results_temp],ignore_index=True)
        performance_results=pd.concat([performance_results,temp_results],ignore_index=True)
        
        
    return Cyc_results,deg_results,performance_results
  



