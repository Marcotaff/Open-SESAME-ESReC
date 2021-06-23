# -*- coding: utf-8 -*-
"""
Created on Fri May 28 07:36:07 2021

@author: blm8
"""

from cell import Cell
import pandas as pd
import matplotlib.pyplot as plt

from performance_analysis import performance_analysis


#Test function 
result=pd.DataFrame()


result["SoC"]=[0.5]
result["SoR"]=[1]
result["SoH"]=[1]
result["Q"]=[10]
result["Capacity"]=[50]


path='//bfhfilerbe01.bfh.ch/blm8/Documents/MT/Open_Sesame/develeopment/test_input2.csv'
data = pd.read_csv(path, delimiter=';')


lim_Mode=2
SoC_max=1
SoC_min=0


temps=performance_analysis(data,result,SoC_max,SoC_min,lim_Mode)

result=temps 




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

