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
    
    input_parameter=input_parameter

    fraction_size=              input_parameter.fraction_size  #resolutio
    select_fraction_type=       input_parameter.select_fraction_type # remooving 
    Initial_SoC=                input_parameter.initial_SoC
    SoC_max=                    input_parameter.SoC_max
    SoC_min=                    input_parameter.SoC_min
    Initial_Temp=               input_parameter.initial_Temp
    Initial_SoR=                input_parameter.initial_SoR
    Initial_SoH=                input_parameter.initial_SoH
    Initial_Capacity=           input_parameter.initial_Capacity #Nominal Capacity 
    lim_Mode=                   input_parameter.lim_Mode # 
    Unom=                       input_parameter.Unom
    Initial_Q=                  input_parameter.initial_Q
    Cell_chemistry=             input_parameter.Cell_chemistry
    timeresolution=             input_parameter.timeresolution
    
    #_______________________________________________________________________________________________
    # Building Class Objects 
    
    #Cell obj
    Cell_Obj=Cell(Initial_SoC,Initial_Temp,Initial_SoR,Initial_SoH,Initial_Capacity,lim_Mode,Initial_Q)      

    #Degradation obj
    Bat_deg= degradation(Cell_chemistry,timeresolution)

    #_______________________________________________________________________________________________
    # Prepare input 
    
    inputdata_len=len(data)
    
    results=np.zeros((len(data),6))
    
    if select_fraction_type == 1:
        
        amount_fractions=math.ceil(inputdata_len/fraction_size)
       
    #Gets cleared 
    if select_fraction_type == 2:
        
        print("not ready")
        #path='//bfhfilerbe01.bfh.ch/blm8/Documents/MT/Open_Sesame/develeopment/variable_fractions.csv'
        #fraction_steps_data = pd.read_csv(path, delimiter=';') 
        
        #amount_fractions=len(fraction_steps_data)
      
    #_______________________________________________________________________________________________
    #Building fractions of input-data and looping threw
    
    start_index=1
    
    Cyc_results=pd.DataFrame()
    deg_results=pd.DataFrame()
  
    
    for i in range(1,int(amount_fractions)+1):
        
      
        #Fractioning mode 2
        if select_fraction_type == 1:
            
            end_index=start_index+fraction_size-1
            
            #Check if end_index in range of input_data
            if end_index > inputdata_len:
                end_index=inputdata_len
            
            #Fraction the data 
            fraction_data=data.loc[(data['time'] >= start_index) & (data['time'] <= end_index)]
            
            start_index=end_index+1
        
        #Fractioning mode 2
        if select_fraction_type == 2:
            
            print("not ready")
            #Read start and end index
            #start_index=fraction_steps_data.start.iloc[i-1] 
            #end_index=fraction_steps_data.end.iloc[i-1]
        
            #Fraction the data 
            #fraction_data=inputdata.loc[(inputdata['time'] >= start_index) & (inputdata['time'] <= end_index)]
        
        
        #_______________________________________________________________________________________________
        #Performance Analysis
        temp_results_np=np.zeros((len(fraction_data),8)) #Create temperorary result array
        
        for x in range(0,len(fraction_data)):
        
            power=fraction_data.power.to_numpy()
            temperature=fraction_data.temperature.to_numpy()
    
            print(temperature[x])
            #Get circuit parameters 
            r_ref=1 #??????????????????????
            Resistance=1#Bat_deg.Chemistry_obj.RfromTempSoC(Cell_Obj.SoC,temperature[x],r_ref)
            OCVoltage=Bat_deg.Chemistry_obj.OCVfromSoC(Cell_Obj.SoC) #SoC value of the timestep before 
            Vmax=Bat_deg.Chemistry_obj.vMax
            Vmin=Bat_deg.Chemistry_obj.vMin
        
            Cell_Obj.CheckV(Resistance,power[x],OCVoltage,Vmax,Vmin)
            Cell_Obj.CalSoC(power[x],timeresolution,SoC_max,SoC_min)
            
            
            #save results of fracment
            temp_results_np[x]=[Cell_Obj.SoC,Cell_Obj.Crate,OCVoltage,Cell_Obj.Vinst,Cell_Obj.updated_current,Resistance,Cell_Obj.limCheckV,Cell_Obj.limCheckSoC]
            
        temp_results = pd.DataFrame(temp_results_np, columns = ['Cell_Obj.SoC','Cell_Obj.Crate','OCV_voltage','V_Bat','I_Updated','Resistance','limChekV','limCHeckSoC'])
        
        
        #_______________________________________________________________________________________________
        #degradation Analysis
    
        Cyc_results_temp,deg_results_temp =Bat_deg.compute(temp_results_np[:,0],temp_results_np[:,1],temperature,start_index)
        
        #_______________________________________________________________________________________________
        #Update SoH and SoR 
        
        Cell_Obj.SoH=Cell_Obj.SoH-Bat_deg.delta_SoH/100
        Cell_Obj.SoR=Cell_Obj.SoR+Bat_deg.delta_SoR/100
        
        print(Cell_Obj.SoH)
        
        #_______________________________________________________________________________________________
        #Save Results 
    
        #Save results i arrays 
        Cyc_results=pd.concat([Cyc_results,Cyc_results_temp])
        deg_results=pd.concat([deg_results,deg_results_temp])
    
     
    
    return Cyc_results,deg_results
  


'''
##Test function 

input_parameter=pd.DataFrame()
input_parameter.fraction_size=100
input_parameter.select_fraction_type=1
input_parameter.initial_SoC=0.77
input_parameter.SoC_max=0.8
input_parameter.SoC_min=0.1
input_parameter.initial_Temp=20
input_parameter.initial_SoR=1
input_parameter.initial_SoH=1
input_parameter.initial_Capacity=50
input_parameter.lim_Mode=1
input_parameter.Unom=3.8
input_parameter.initial_Q=10
input_parameter.Cell_chemistry="NMC"
input_parameter.timeresolution=1
input_parameter.timeresolution=1


path='//bfhfilerbe01.bfh.ch/blm8/Documents/MT/Open_Sesame/develeopment/test_input2.csv'
data = pd.read_csv(path, delimiter=';')


simulation(data,input_parameter)
'''




