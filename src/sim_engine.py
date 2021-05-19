
'''
Simulation Engine 

'''
#import chemicallibrary_NMC
import pandas as pd
import math

#-----------------------------------------------------------------------------------------
#Parameters 

fraction_size=31  #amount of timestamps 
select_fraction_type=1      #1 == fixed length
                            #2 == according to file
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
        
        
        #To do 
        #Return simulation results of fraction 
        #Add them to Resultarray
  
    print(fraction_data)
        
        
        
    










