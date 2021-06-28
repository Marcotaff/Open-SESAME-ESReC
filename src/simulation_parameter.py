import pandas as pd



def get_simulation_parameter(nominal_energy, 
                             Cell_chemistry="NMC", 
                             timeresolution=1,
                             repetition = 0,  
                             initial_SoC=1, SoC_max=1, SoC_min=0):
    
    parameter=pd.DataFrame()
    
    parameter.Cell_chemistry=Cell_chemistry
    parameter.timeresolution=timeresolution      #seconds per step
    parameter.repetition = repetition            #how many times the input is repeated
    
    parameter.fraction_size=13
    parameter.initial_SoC=initial_SoC
    parameter.SoC_max=SoC_max
    parameter.SoC_min=SoC_min
    parameter.initial_Temp=20           #why not taking the first value of temperature input vector?
    parameter.initial_SoR=1
    parameter.initial_SoH=1
    parameter.nominal_energy=nominal_energy  #Wh

    parameter.lim_Mode=1
    parameter.select_fraction_type=1  #todo:remove
    parameter.Unom=3.8                #todo:move to chemical library
    parameter.initial_Q=10            #todo: check if it is not possible to base on initial_SoC and initial_SoH. Everything should be normalized in the end.
    
    return parameter