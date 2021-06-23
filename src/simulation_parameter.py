import pandas as pd



def get_simulation_parameter(initial_SoC=1, SoC_max=1, SoC_min=0, Cell_chemistry="NMC"):
    #todo: extend parameter list
    
    parameter=pd.DataFrame()
    parameter.fraction_size=100
    parameter.select_fraction_type=1
    parameter.initial_SoC=initial_SoC
    parameter.SoC_max=SoC_max
    parameter.SoC_min=SoC_min
    parameter.initial_Temp=20
    parameter.initial_SoR=1
    parameter.initial_SoH=1
    parameter.initial_Capacity=50       #why not use initial SOH and nominal capacity?  
    parameter.lim_Mode=1
    parameter.Unom=3.8
    parameter.initial_Q=10
    parameter.Cell_chemistry=Cell_chemistry
    parameter.timeresolution=1
    
    return parameter