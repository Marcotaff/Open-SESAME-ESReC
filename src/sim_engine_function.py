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
    
    data.power_W=data.power_W/1000
    
    
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
        
        progress=round((i/amount_fractions)*100,2)
        print("progress:",progress,"%")
        #_______________________________________________________________________________________________
        #Performance Analysis
        temp_results_np=np.zeros((len(fraction_power),15)) #Create temperorary result array
        
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
            
            Cell_Obj.Power_upd=Cell_Obj.Power_upd*1000
            
            #save results of fragment
            temp_results_np[x]=[Cell_Obj.SoR,Cell_Obj.SoH,Cell_Obj.SoC,Cell_Obj.Crate,Cell_Obj.Power_upd,OCVoltage,Cell_Obj.Vinst,Cell_Obj.updated_current,Resistance,Cell_Obj.limCheckV,Cell_Obj.limCheckSoC,bat_temp,fraction_power[x]*1000,Cell_Obj.act_Energy,Cell_Obj.act_Q]    
            
            
       
        
        #_______________________________________________________________________________________________
        #degradation Analysis
      
        Cyc_results_temp,deg_results_temp =Bat_deg.compute(temp_results_np[:,2],temp_results_np[:,3],fraction_Tambient[:],index_cyc)
        #_______________________________________________________________________________________________
        #Update SoH and SoR 
    
        Cell_Obj.update(Bat_deg.delta_SoH,Bat_deg.delta_SoR)
    

        #_______________________________________________________________________________________________
        #Save Results 
    
        #Save results i arrays 
        
        if i==0:
            Cyc_results=Cyc_results_temp
            deg_results=deg_results_temp
            performance_results=temp_results_np
            
        else:
            Cyc_results=np.concatenate((Cyc_results,Cyc_results_temp), axis=0)
            deg_results=np.concatenate((deg_results,deg_results_temp), axis=0)
            performance_results=np.concatenate((performance_results,temp_results_np), axis=0)
        
        
        #Cyc_results=pd.concat([Cyc_results,Cyc_results_temp],ignore_index=True)
        #deg_results=pd.concat([deg_results,deg_results_temp],ignore_index=True)
        #performance_results=pd.concat([performance_results,temp_results],ignore_index=True)
        
        
        
    columns = ['DoD','half/full','start_indx','end_indx','AVG_SoC','AVG_Crate','Info1','AVG_Temp','SF_DoD','SF_Crate','IMP_AVGSoC','Imp_Temp','SF_cyc_sum','Tot_cyc','R_SF_Dod','R_SF_Crate','R_SF_AVGSoC','R_SoR_sum','Tot_Sor_cycle']
    Cyc_results = pd.DataFrame(Cyc_results, columns = columns )  
        
    columns = ['SF_Cal_SoC','SF_Cal_Temp','Tot_Cal','ToT_Cyc','Sum_Deg','Tot_SoR']    
    Cyc_results = pd.DataFrame(Cyc_results, columns = columns )  


    columns = ['SoR','SoH','SoC','Crate','power_upd','OCV_voltage','V_Bat','I_Updated','Resistance','limChekV','limCHeckSoC','Bat_temp','power_sim_in','Act_Energy','Act_Q']
    performance_results = pd.DataFrame(performance_results, columns = columns )
      
        
        
    
        
    return Cyc_results,deg_results,performance_results
 
    
''' 

def quick_simulation(data,input_parameter):
    
    
    Perf_Result_list = list()
    Cyc_Result_list = list()
    Deg_Result_list = list()
    
    entry_break=0
    #_______________________________________________________________________________________________
    # check if full or aprox simulation 
    
    if input_parameter.SoH_repeatsim == 0:
        
        aprox_sim=0     
    else: 
         aprox_sim=1
        
   
    act_repetition=1 # repetition variable 
    
    while act_repetition <=input_parameter.repetition:
        
        
    
        data.power_W=data.power_W/1000
        
        #_______________________________________________________________________________________________
        # Building Class Objects 
        
        if act_repetition==1:
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
        #predefine output arrays
    
        inputdata_len=len(data.power_W)
        amount_fractions=math.ceil(inputdata_len/input_parameter.fraction_size)
        start_index=0
        
        #_______________________________________________________________________________________________
        # Looping threw fractions 
       
        start_SoH=Cell_Obj.SoH
        start_SoR=Cell_Obj.SoR
    
    
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
            
            #progress=round((i/amount_fractions)*100,2)
            #print("progress:",progress,"%")
            #_______________________________________________________________________________________________
            #Performance Analysis
            temp_results_np=np.zeros((len(fraction_power),15)) #Create temperorary result array
            
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
                
                Cell_Obj.Power_upd=Cell_Obj.Power_upd*1000
                
                #save results of fragment
                temp_results_np[x]=[Cell_Obj.SoR,Cell_Obj.SoH,Cell_Obj.SoC,Cell_Obj.Crate,Cell_Obj.Power_upd,OCVoltage,Cell_Obj.Vinst,Cell_Obj.updated_current,Resistance,Cell_Obj.limCheckV,Cell_Obj.limCheckSoC,bat_temp,fraction_power[x]*1000,Cell_Obj.act_Energy,Cell_Obj.act_Q]   
            
            #_______________________________________________________________________________________________
            #degradation Analysis
          
            Cyc_results_temp,deg_results_temp =Bat_deg.compute(temp_results_np[:,2],temp_results_np[:,3],fraction_Tambient[:],index_cyc)
            
            #_______________________________________________________________________________________________
            #Update SoH and SoR 
        
            Cell_Obj.update(Bat_deg.delta_SoH,Bat_deg.delta_SoR)
        
            #_______________________________________________________________________________________________
            #Save Results 
        
            if i==0:
                Cyc_results=Cyc_results_temp
                deg_results=deg_results_temp
                performance_results=temp_results_np
            
            else:
                Cyc_results=np.concatenate((Cyc_results,Cyc_results_temp), axis=0)
                deg_results=np.concatenate((deg_results,deg_results_temp), axis=0)
                performance_results=np.concatenate((performance_results,temp_results_np), axis=0)
                
      
    
        #_______________________________________________________________________________________________
        #pass on key results to next repetition  
            
        #delta SoH per repetition  
        end_SoH=Cell_Obj.SoH
        end_SoR=Cell_Obj.SoR
        
        delta_SoH=start_SoH-end_SoH 
        
        
        delta_SoR=end_SoR-start_SoR
        
        #keep simulated SoC for the next repetition or not 
        if input_parameter.keep_rep_SoC == 0:
            
            Cell_Obj.SoC=input_parameter.initial_SoC
            
            
        if aprox_sim == 1:
        
            #calc actual repetition
            
            
            nr_repetition=round(input_parameter.SoH_repeatsim/delta_SoH,0)
            act_repetition= act_repetition+nr_repetition
            
            Cell_Obj.update(nr_repetition*delta_SoH,nr_repetition*delta_SoR)
            
            
            if act_repetition > input_parameter.repetition:
                
                if entry_break==1:
                    
                    print("Entrybreak!")
                    break
                    
                
                if entry_break==0:
                    act_repetition=input_parameter.repetition
                    entry_break=entry_break+1
                    
                
        
        
        if aprox_sim == 0:
            
            
             act_repetition=act_repetition+1
             nr_repetition=1            
   
        
        
        
        
        columns = ['SF_DoD','SF_Crate','SF_AVGSoC','SF_Temp','SF_cyc_sum','Tot_SoH_cyc','R_SF_DoD','R_SF_Crate','R_SF_AVGSoC','R_SoR_Sum','Tot_SoR_cycle','CC_DoD','CC_Full_half_c','CC_startindex','CC_endindex','CC_AVG_SoC','CC_AVG_Crate','CC_info','CC_AVG_Temp']  
        Cyc_results = pd.DataFrame(Cyc_results, columns = columns )  
        Cyc_results["calculation_iteration"]=act_repetition
        
        
        columns = ['SF_Cal_SoC','SF_Cal_Temp','SoH_Tot_Cal','SoH_ToT_Cyc','SoH_sum_degr','SoR_ToT_Cyc','SoR_sum_degr','R_SF_Cal_SoC','R_SF_Cal_Temp','R_Tot_cal']
        deg_results = pd.DataFrame(deg_results, columns = columns )  
        deg_results["calculation_iteration"]=act_repetition

        columns = ['SoR','SoH','SoC','Crate','power_upd','OCV_voltage','V_Bat','I_Updated','Resistance','limChekV','limCHeckSoC','Bat_temp','power_sim_in','Act_Energy','Act_Q']
        performance_results = pd.DataFrame(performance_results, columns = columns )
        performance_results["calculation_iteration"]=act_repetition
            
        Perf_Result_list.append(performance_results)    
        Cyc_Result_list.append( Cyc_results) 
        Deg_Result_list.append(deg_results)  
        
        
        
       
        print("---------------------------------------")
        print("entrybreak.",entry_break) 
        print("nr_repetition:",nr_repetition)
        print("Current repetition:", act_repetition-1 )
        print(performance_results.SoH.iloc[-1])
      
      
      
        Output=[Perf_Result_list,Cyc_Result_list, Deg_Result_list]
      
       
      
        
    return Output
  
'''  

def quick_simulation(data,input_parameter):
    
    
    Perf_Result_list = list()
    Cyc_Result_list = list()
    Deg_Result_list = list()
    
    entry_break=0
    #_______________________________________________________________________________________________
    # check if full or aprox simulation 
    
    act_repetition=1 # repetition variable 
    
    data.power_W=data.power_W*1.1/1000
    
    while act_repetition <=input_parameter.iteration:
     
    
      
       
        
        #_______________________________________________________________________________________________
        # Building Class Objects 
        
        if act_repetition==1:
            #Degradation obj
            Bat_deg= degradation(input_parameter.Cell_chemistry,input_parameter.timeresolution,input_parameter.cyc_count_alg)
             
            #Cell 
            initial_Bat_temp=data.ambient_temperature_C[0] 
            Cell_Obj=Cell(input_parameter.initial_SoC,initial_Bat_temp,input_parameter.initial_SoR,input_parameter.initial_SoH,input_parameter.nominal_energy,input_parameter.lim_Mode,Bat_deg.Chemistry_obj.Q)
        
        print(act_repetition)
        #_______________________________________________________________________________________________
        #predefine output arrays
        
        Cyc_results=pd.DataFrame()
        deg_results=pd.DataFrame()
        performance_results=pd.DataFrame()
  
        #_______________________________________________________________________________________________
        #predefine output arrays
    
        inputdata_len=len(data.power_W)
        amount_fractions=math.ceil(inputdata_len/input_parameter.fraction_size)
        start_index=0
        
        #_______________________________________________________________________________________________
        # Looping threw fractions 
       
        start_SoH=Cell_Obj.SoH
        start_SoR=Cell_Obj.SoR
    
    
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
            
           
            #progress=round((i/amount_fractions)*100,2)
            #print("progress:",progress,"%")
            #_______________________________________________________________________________________________
            #Performance Analysis
            temp_results_np=np.zeros((len(fraction_power),15)) #Create temperorary result array
            
            for x in range(0,len(fraction_power)):
            
                #Temperature Model
                bat_temp=fraction_Tambient[x] # ambient temp == bat temp 
                
                #Get circuit parameters 
                Resistance=Bat_deg.Chemistry_obj.RfromTempSoC(Cell_Obj.SoC,bat_temp)
                OCVoltage=Bat_deg.Chemistry_obj.OCVfromSoC(Cell_Obj.SoC) #SoC value of the timestep before 
                Vmax=Bat_deg.Chemistry_obj.vMax
                Vmin=Bat_deg.Chemistry_obj.vMin
            
                #Check Voltage and SoC limits
                Cell_Obj.CheckV(Resistance,fraction_power[x],OCVoltage,Vmax,Vmin)
                Cell_Obj.CalSoC(Cell_Obj.Power_upd,input_parameter.timeresolution,input_parameter.SoC_max,input_parameter.SoC_min)
                
                Cell_Obj.Power_upd=Cell_Obj.Power_upd*1000
                
                #save results of fragment
                temp_results_np[x]=[Cell_Obj.SoR,Cell_Obj.SoH,Cell_Obj.SoC,Cell_Obj.Crate,Cell_Obj.Power_upd,OCVoltage,Cell_Obj.Vinst,Cell_Obj.updated_current,Resistance,Cell_Obj.limCheckV,Cell_Obj.limCheckSoC,bat_temp,fraction_power[x]*1000,Cell_Obj.act_Energy,Cell_Obj.act_Q]   
                
            #_______________________________________________________________________________________________
            #degradation Analysis
            Cyc_results_temp,deg_results_temp =Bat_deg.compute(temp_results_np[:,2],temp_results_np[:,3],fraction_Tambient[:],index_cyc)
            #_______________________________________________________________________________________________
            #Update SoH and SoR 
            Cell_Obj.update(Bat_deg.delta_SoH,Bat_deg.delta_SoR)
            
            
            #_______________________________________________________________________________________________
            #Save Results 
        
            if i==0:
                Cyc_results=Cyc_results_temp
                deg_results=deg_results_temp
                performance_results=temp_results_np
            
            else:
                Cyc_results=np.concatenate((Cyc_results,Cyc_results_temp), axis=0)
                deg_results=np.concatenate((deg_results,deg_results_temp), axis=0)
                performance_results=np.concatenate((performance_results,temp_results_np), axis=0)
            
        #_______________________________________________________________________________________________
        #pass on key results to next repetition  
            
        #delta SoH and SoR of the current repetition 
        delta_SoH=start_SoH-Cell_Obj.SoH
        delta_SoR=Cell_Obj.SoR-start_SoR
        
        #keep simulated SoC for the next repetition or not 
        if input_parameter.keep_rep_SoC == 0:
            Cell_Obj.SoC=input_parameter.initial_SoC
        
        #_______________________________________________________________________________________________
        #Save Results  
        columns = ['SF_DoD','SF_Crate','SF_AVGSoC','SF_Temp','SF_cyc_sum','Tot_SoH_cyc','R_SF_DoD','R_SF_Crate','R_SF_AVGSoC','R_SoR_Sum','Tot_SoR_cycle','CC_DoD','CC_Full_half_c','CC_startindex','CC_endindex','CC_AVG_SoC','CC_AVG_Crate','CC_info','CC_AVG_Temp']  
        Cyc_results = pd.DataFrame(Cyc_results, columns = columns )  
        Cyc_results["calculation_iteration"]=act_repetition
        
        
        columns = ['SF_Cal_SoC','SF_Cal_Temp','SoH_ToT_Cal','SoH_ToT_Cyc','SoH_sum_degr','SoR_ToT_Cyc','SoR_sum_degr','R_SF_Cal_SoC','R_SF_Cal_Temp','R_Tot_cal']
        deg_results = pd.DataFrame(deg_results, columns = columns )  
        deg_results["calculation_iteration"]=act_repetition

        columns = ['SoR','SoH','SoC','Crate','power_upd','OCV_voltage','V_Bat','I_Updated','Resistance','limChekV','limCHeckSoC','Bat_temp','power_sim_in','Act_Energy','Act_Q']
        performance_results = pd.DataFrame(performance_results, columns = columns )
        performance_results["calculation_iteration"]=act_repetition
            
        Perf_Result_list.append(performance_results)    
        Cyc_Result_list.append( Cyc_results) 
        Deg_Result_list.append(deg_results)  
        
        SoH_anFANG=performance_results.SoH.iloc[0]
        SoH_ende=performance_results.SoH.iloc[-1]
        
        
       
        
        print("---------------------------------------")
         
        print("act repetition:", act_repetition )
        print(performance_results.SoH.iloc[-1]) 
        
        
    
        if input_parameter.SoH_repeatsim != 0:
        
            #calc actual repetition
            
            
            nr_repetition=round(input_parameter.SoH_repeatsim/delta_SoH,0)
            act_repetition_old=act_repetition
            act_repetition= act_repetition+nr_repetition
            
           
            
            
            if act_repetition > input_parameter.iteration:
                
                if entry_break==1:
                    
                   
                    break
                    
                if entry_break==0:
                    
                    act_repetition=input_parameter.iteration
                    entry_break=entry_break+1
                    nr_repetition=input_parameter.iteration-act_repetition_old
                        
            Cell_Obj.update(nr_repetition*delta_SoH,nr_repetition*delta_SoR)     
        
        
        if input_parameter.SoH_repeatsim == 0:
            
             act_repetition=act_repetition+1
             nr_repetition=1            
   
       
      
      
      
        Output=[Perf_Result_list,Cyc_Result_list, Deg_Result_list]
      
       
      
        
    return Output 
  