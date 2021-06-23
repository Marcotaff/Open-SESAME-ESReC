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
    
    fraction_size=              input_parameter.fraction_size
    select_fraction_type=       input_parameter.select_fraction_type
    Initial_SoC=                input_parameter.initial_SoC
    SoC_max=                    input_parameter.SoC_max
    SoC_min=                    input_parameter.SoC_min
    Initial_Temp=               input_parameter.initial_Temp
    Initial_SoR=                input_parameter.initial_SoR
    Initial_SoH=                input_parameter.initial_SoH
    Initial_Capacity=           input_parameter.initial_Capacity
    lim_Mode=                   input_parameter.lim_Mode
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
        
    if select_fraction_type == 2:
        
        print("not ready")
        #path='//bfhfilerbe01.bfh.ch/blm8/Documents/MT/Open_Sesame/develeopment/variable_fractions.csv'
        #fraction_steps_data = pd.read_csv(path, delimiter=';') 
        
        #amount_fractions=len(fraction_steps_data)
      
    #-----------------------------------------------------------------------------------------
    #Building fractions of input-data and looping threw
    
    start_index=1
    
    
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
        
        
        #-----------------------------------------------------------------------------------------
        #Performance Analysis
        
        for x in range(0,len(fraction_data)):
        
            power=fraction_data.power.to_numpy()
            temperature=fraction_data.temperature.to_numpy()
    
            temp_results=np.zeros((len(fraction_data),6))
    
            #Wird noch ersetzt mit dem chemicallibrary funktionen
            Resistance=0.001
            OCVoltage=4
            Vmax=4.3
            Vmin=2.3
        
            Cell_Obj.CheckV(Resistance,power[x],OCVoltage,Vmax,Vmin)
            Cell_Obj.CalSoC(power[x],timeresolution,SoC_max,SoC_min)
        
            #save results of fracment 
            temp_results[x]=[OCVoltage,Cell_Obj.Vinst,Cell_Obj.updated_current,Resistance,Cell_Obj.limCheckV,Cell_Obj.limCheckSoC]
       
        

            
    
    return 
  




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
    
    
    
#-----------------------------------------------------------------------------------------
#Simulation Parameters 

fraction_size=100  #amount of timestamps 
select_fraction_type=1      #1 == fixed length
                            #2 == according to file
Initial_SoC =   0.77
SoC_max =       0.8
SoC_min =       0.0

Initial_Temp=   20

Initial_SoR  =  1
Initial_SoH  =   1 
Initial_Capacity = 50 #kwh 

lim_Mode  =     1
Unom =          3.8 
Initial_Q=      10                            
 
#-----------------------------------------------------------------------------------------
#Built Cell element 
Cell=Cell(Initial_SoC,Initial_Temp,Initial_SoR,Initial_SoH,Initial_Capacity,lim_Mode,Initial_Q)                       

#-----------------------------------------------------------------------------------------
#Read input file 

path='//bfhfilerbe01.bfh.ch/blm8/Documents/MT/Open_Sesame/develeopment/test_input2.csv'
inputdata = pd.read_csv(path, delimiter=';')

inputdata_len=len(inputdata)

#-----------------------------------------------------------------------------------------
#Building up fraction-loop

if select_fraction_type == 1:
    
    amount_fractions=math.ceil(inputdata_len/fraction_size)
    
if select_fraction_type == 2:
    
    path='//bfhfilerbe01.bfh.ch/blm8/Documents/MT/Open_Sesame/develeopment/variable_fractions.csv'
    fraction_steps_data = pd.read_csv(path, delimiter=';') 
    
    amount_fractions=len(fraction_steps_data)
    
#-----------------------------------------------------------------------------------------
#Building fractions of input-data and looping threw

start_index=1

results=pd.DataFrame()

for i in range(1,int(amount_fractions)+1):
    
  
    #Fractioning mode 2
    if select_fraction_type == 1:
        
        end_index=start_index+fraction_size-1
        
        #Check if end_index in range of input_data
        if end_index > inputdata_len:
            end_index=inputdata_len
        
        #Fraction the data 
        fraction_data=inputdata.loc[(inputdata['time'] >= start_index) & (inputdata['time'] <= end_index)]
        
        start_index=end_index+1
    
    #Fractioning mode 2
    if select_fraction_type == 2:
        
        #Read start and end index
        start_index=fraction_steps_data.start.iloc[i-1] 
        end_index=fraction_steps_data.end.iloc[i-1]
    
        #Fraction the data 
        fraction_data=inputdata.loc[(inputdata['time'] >= start_index) & (inputdata['time'] <= end_index)]
    
    

    #-----------------------------------------------------------------------------------------
    #Performance Analysis
    
    if i ==1:
        results["SoC"]=[Initial_SoC]
        results["SoR"]=[Initial_SoR]
        results["SoH"]=[Initial_SoH]
        results["Q"]=[Initial_Q]
        results["Capacity"]=[Initial_Capacity]
    
    SoC_max=SoC_max
    SoC_min=SoC_min
    lim_Mode=1
    
    timeresolution=1 #SeC
    temps=performance_analysis(fraction_data,results,SoC_max,SoC_min,lim_Mode,timeresolution)
  
    
    results=pd.concat([results, temps],ignore_index = True)
    
    
      
    
  

fig, axs = plt.subplots(3,1, sharex=True)
fig.subplots_adjust(hspace=0)
axs[0].plot(results["SoC"])
axs[0].set_ylabel('SoC')
axs[0].grid(True)

axs[1].scatter(results.index,results["C-Rate"])
axs[1].set_ylabel('C-Rate')
axs[1].grid(True)

      
axs[2].plot(results["Cell_Voltage"])
axs[2].set_ylabel('Cell_Voltage [V]')
axs[2].grid(True)

fig.tight_layout()

plt.show()



results.to_csv('//bfhfilerbe01.bfh.ch/blm8/Documents/MT/Open_Sesame/develeopment/Resultate_temp.csv')        
'''