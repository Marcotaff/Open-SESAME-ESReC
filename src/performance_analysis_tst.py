# -*- coding: utf-8 -*-

import pandas as pd
from cell import Cell

import matplotlib.pyplot as plt


data=pd.read_csv('C:/local_data/Open-SESAME-ESReC/src/test_file.csv', delimiter=',')
len_data=len(data)

#Create object

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
Resistance=0.009

OCVoltage=3.8
Vmax=4.3
Vmin=3.2
deltaT=10#Sec


test_Cell=Cell(initial_SoC,initial_Temp,Initial_SoR,inital_SoH,initial_Capacity,lim_Mode,initial_Q)


result=pd.DataFrame(columns=range(len_data))
result["SoC","Cell_Voltage","Cell_Current","C-Rate"]=0
result["V_lim","SoC-lim"]=False

for x in range(0,len_data):
    
    test_Cell.CheckV(Resistance,data.Power.iloc[x],OCVoltage,Vmax,Vmin)
    test_Cell.CalSoC(data.Power.iloc[x],deltaT,SoC_max,SoC_min)

    
    result.loc[x,'SoC']=test_Cell.SoC
    result.loc[x,'Cell_Voltage']=test_Cell.Vinst
    result.loc[x,'Cell_Current']=test_Cell.updated_current
    result.loc[x,'C-Rate']=test_Cell.Crate
    result.loc[x,'V-lim']=test_Cell.limCheckV
    
    
    result.loc[x,'SoC-lim']=test_Cell.limCheckSoC
    
    
    
    
    




fig, axs = plt.subplots(3,1, sharex=True)
fig.subplots_adjust(hspace=0)
axs[0].plot(result["SoC"])
axs[0].set_ylabel('SoC')
axs[0].grid(True)

axs[1].scatter(result.index,result["C-Rate"])
axs[1].set_ylabel('C-Rate')
axs[1].grid(True)

      
axs[2].plot(result["Cell_Voltage"])
axs[2].set_ylabel('Cell_Voltage [V]')
axs[2].grid(True)

fig.tight_layout()

plt.show()




