import pandas as pd
import sys
from sys import exit


def get_simulation_parameter(nominal_energy, 
                             Cell_chemistry="NMC", 
                             timeresolution=60,
                             iteration =1000, #Anzahl Berechnungen  
                             initial_SoC=0.5, SoC_max=1, SoC_min=0,
                             SoH_repeatsim=0.01
                             ):
    
    parameter=pd.DataFrame()
    
    #SoC related Parameters 
    parameter.SoC_max=SoC_max

    parameter.SoC_min=SoC_min 
    parameter.initial_SoC=initial_SoC
    
    #Battery related parameters 
    parameter.Cell_chemistry=Cell_chemistry
    parameter.initial_SoR=1
    parameter.initial_SoH=1
    parameter.nominal_energy=nominal_energy  #Wh
    
    #Simulation Parameters 
    parameter.timeresolution=timeresolution   
    parameter.iteration = iteration 
    parameter.fraction_size=1440
    parameter.lim_Mode=2             #select between one and two 
    parameter.cyc_count_alg=1 #1= Rainflow, 2=Peakt to Peak
    parameter.SoH_repeatsim=SoH_repeatsim  
    parameter.keep_rep_SoC=0    
    
    
    #Battery size in kWh from Wh
    parameter.nominal_energy=parameter.nominal_energy/1000
    
    
    
    #Input Parameter Check
    param_check=check_parameters(parameter)
    if param_check >0:
        exit(0)
        
    
    
    return parameter


def check_parameters(param):
    flag = 0
    if param.Cell_chemistry not in ("NMC","LTO"):
        print("ERROR: Cell chemistry invalid or not available. Make sure cell chemistry is in capital letters")
        flag = flag + 1
    if param.timeresolution <= 0 or isinstance(param.timeresolution, float) :
        print("ERROR: Time resolution is either <= 0 or is a float value. Please set an interger value greater than 0")
        flag = flag + 1
    if param.iteration < 0:
        print("ERROR: Repetitions are lesser than 0. Please set a value >= 0")
        flag = flag + 1
    if param.initial_SoC < 0 or param.SoC_max < 0 or param.SoC_min < 0 or param.initial_SoC > 1 or param.SoC_max > 1 or param.SoC_min > 1:
        print("ERROR: One or more of inital SoC, SoC_max and SoC_min is either < 0 or > 1. Please set a value between and including 0 and 1")
        flag = flag + 1
    if param.initial_SoC > param.SoC_max or param.initial_SoC < param.SoC_min or param.SoC_min > param.SoC_max:
        print("ERROR: The SoC_min, initial_SoC and SoC_max are not in the correct order. Please check that the values are SoC_min <= initial_SoC <= SoC_max")
        flag = flag + 1
    if param.initial_SoR < 1 or param.initial_SoH > 1:
        print("ERROR: Either initial SoR < 1 or initial SoH > 1. Please ensure that initial SoR >= 1 and initial SoH <= 1")
        flag = flag + 1
    if param.nominal_energy <= 0:
        print("ERROR: Value of nominal energy is <= 0. Please set a value > 0")
        flag = flag + 1
    if param.lim_Mode not in (1,2):
        print("ERROR: lim_Mode has a value other than 1 or 2. Please ensure that the value is either 1 or 2")
        flag = flag + 1
    if param.cyc_count_alg not in (1,2):
        print("ERROR: cyc_count_alg has a value other than 1 or 2. Please ensure that the value is either 1 or 2")
        flag = flag + 1
    if param.fraction_size <=0:
        print("ERROR: Fraction size needs to be bigger than Zero")
        flag = flag + 1
    if param.keep_rep_SoC not in (0,1):   
        print("ERROR: Parameter keep-rep-SoC needs to be 0 or 1")
        flag = flag + 1
    if param.SoH_repeatsim >=0.05:   
            print("ERROR: SoH_repeat_sim needs to be smaller than 0.05 (5%SoH)-Simulation jumps bigger than 5% SoH are leading to inacucrate results")
            flag = flag + 1         
    if param.SoH_repeatsim <0:
           print("ERROR: SoH_repeat_sim can not be negativ")
           flag = flag + 1  
    if flag > 0:
        print("Please make the above changes and run again")
        
        
        
    return flag
        