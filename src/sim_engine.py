
'''
Simulation Engine 

'''
#import chemicallibrary_NMC
import pandas as pd
from cell import Cell
import math

#-----------------------------------------------------------------------------------------
#Simulation Parameters 

fraction_size=31  #amount of timestamps 
select_fraction_type=1      #1 == fixed length
                            #2 == according to file
initial_SoC =   0.77
SoC_max =       0.8
SoC_min =       0.0

initial_Temp=   20

Initial_SoR  =  1
inital_SoH  =   1 
initial_Capacity = 50 #kwh 

lim_Mode  =     1
Unom =          3.8 
initial_Q=      10                            
 
#-----------------------------------------------------------------------------------------
#Built Cell element 
Cell=Cell(initial_SoC,initial_Temp,Initial_SoR,inital_SoH,initial_Capacity,SoC_max,SoC_min,lim_Mode,Unom,initial_Q)                       

#-----------------------------------------------------------------------------------------
#Read input file 

path='//bfhfilerbe01.bfh.ch/blm8/Documents/MT/Open_Sesame/develeopment/test_input.csv'
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
    
    #get resistance 
    #Resistance=RfromTempSoC(soc, temp, r_ref)
    Resistance=0.0001
    
    
    Cell.CheckV(Resistance,data.Power.iloc[i],OCVoltage,Vmax,Vmin)
    Cell.CalSoC(data.Power.iloc[i],deltaT,SoC_max,SoC_min)
        
        
        
        
  
 
        
        
        
    










