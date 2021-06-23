
'''
Simulation Engine 

'''
#import chemicallibrary_NMC
import pandas as pd
from cell import Cell
import math
from performance_analysis import performance_analysis
import matplotlib.pyplot as plt

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
        
        
  
 
        
        
        
    










