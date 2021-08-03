# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 14:04:23 2021

@author: blm8
"""

import pandas as pd
from simulation_input import simulation_input
from simulation_output import simulation_output
import simulation_parameter
import sim_engine_function
import matplotlib.pyplot as plt


plt.close('all')



#Define a input object 
data = simulation_input()
data.read_csv('test_inputdata3.csv')       #read a an input object as csv



own_params = simulation_parameter.get_simulation_parameter(nominal_energy=160,initial_SoC=0.55, SoC_max=1, SoC_min=0, SoH_repeatsim=0.001)
Sim_Results=simulation_output(sim_engine_function.simulation(data,own_params))
Res=Sim_Results.iteration_results(own_params.initial_SoH,own_params.initial_SoR)







#####################################################################################################################################################
#Default Plots 


#SoH and SoR 
fig1, axs = plt.subplots(2,1, sharex=True)
fig1.tight_layout()
fig1.subplots_adjust(hspace=0.08)


axs[0].plot(Res.calculation_iteration,Res.SoH,'ro-',label="Total SoH degradation")
axs[0].plot(Res.calculation_iteration,Res.SoH_cyc,'--o',alpha=0.5,label="SoH degr. caused by Cyclic aging")
axs[0].plot(Res.calculation_iteration,Res.SoH_cal,'--o',alpha=0.5,label="SoH degr. caused by Calandaric aging")
axs[0].legend()
axs[0].set_ylabel('SoH')
axs[0].grid(True)

axs[1].plot(Res.calculation_iteration,Res.SoR_Tot,'go-',label="SoR increasing")
axs[1].legend()
axs[1].set_ylabel('SoR')
axs[1].set_xlabel('Nr. of iterations')
axs[1].grid(True)


plt.legend()
plt.show()


#SoC Plot
Sim_Results.SoC_plt()





