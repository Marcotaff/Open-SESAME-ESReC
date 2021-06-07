# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 13:33:16 2021

@author: blm8
"""

from cell import Cell
import pandas as pd


def performance_analysis(data,resultarray,SoC_max,SoC_min,lim_Mode):

    #create temp resultarray called:
    temp_results=pd.DataFrame()
    
    #Define Columns of array
    temp_results["SoC"]=0
    temp_results["SoR"]=0
    temp_results["SoH"]=0
    temp_results["C-Rate"]=0
    temp_results["Capacity"]=0
    temp_results["Q"]=0
    
    temp_results["Cell_Voltage"]=0
    temp_results["Cell_Current"]=0
    temp_results["Cell_Resistance"]=0
    temp_results["Cell_OCV"]=0
    
    temp_results["V_lim"]=False
    temp_results["SoC_lim"]=False
    initial_Temp=data.temperature.iloc[0]
    

    #-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #Create a cell object 
    Cell_Obj=Cell(resultarray.SoC.iloc[-1],initial_Temp,resultarray.SoR.iloc[-1],resultarray.SoH.iloc[-1],resultarray.Capacity.iloc[-1],lim_Mode,resultarray.Q.iloc[-1])
  
    #-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #Looping threw Calculations 
    
    for x in range(0,len(data)):
        
        print(x)
        #Temp --> later from functions
        Temp=data.temperature.iloc[x]
        
        Resistance=0.001
        OCVoltage=4
        Vmax=4.3
        Vmin=2.3
        
        if x != 0:
            deltaT=data.time.iloc[x]-data.time.iloc[x-1]
        
        if x==0:
            deltaT=data.time.iloc[x]
        
        Cell_Obj.CheckV(Resistance,data.power.iloc[x],OCVoltage,Vmax,Vmin)
        Cell_Obj.CalSoC(data.power.iloc[x],deltaT,SoC_max,SoC_min)
        
        #Save timestep variables 
        temp_results.loc[x,"SoC"]=Cell_Obj.SoC
        temp_results.loc[x,"SoR"]=Cell_Obj.SoR
        temp_results.loc[x,"SoH"]=Cell_Obj.SoH
        temp_results.loc[x,"C-Rate"]=Cell_Obj.Crate
        temp_results.loc[x,"Capacity"]=Cell_Obj.Capacity
        temp_results.loc[x,"Q"]=Cell_Obj.Q
    
        temp_results.loc[x,"Cell_Voltage"]=Cell_Obj.Vinst
        temp_results.loc[x,"Cell_Current"]=Cell_Obj.updated_current
        temp_results.loc[x,"Cell_Resistant"]=Resistance
        temp_results.loc[x,"Cell_OCV"]=OCVoltage
    
        temp_results["V_lim"]=Cell_Obj.limCheckV
        temp_results["SoC_lim"]=Cell_Obj.limCheckSoC  

    
       
    return temp_results