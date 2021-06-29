import pandas as pd

from simulation_input import simulation_input
from simulation_output import simulation_output

import simulation_parameter
import sim_engine_function

import matplotlib.pyplot as plt


plt.close('all')

#default_params = simulation_parameter.get_simulation_parameter(nominal_energy=100)
own_params = simulation_parameter.get_simulation_parameter(nominal_energy=100,initial_SoC=1, SoC_max=1, SoC_min=0)


data = simulation_input()
data.read_csv('test5.csv')       #read a an input object as csv



#for shubham:
#data = myOwnInputManager()   #your fucntion should return a simulation_input object 

#output1 = sim_engine_function.simulation(data, default_params)
#output2 = sim_engine_function.simulation(data, own_params)


#this way 
Results=simulation_output(sim_engine_function.simulation(data,own_params))


#test=Results.create_deg_results(own_params.initial_SoH,own_params.initial_SoR)

Resultarray=Results.get_def_resultarray(own_params.initial_SoH,own_params.initial_SoH)
Results.write_def_csv("outputtest.csv", separator=',')



fig3, axs = plt.subplots(3, 1, sharex=True)
    
fig3.tight_layout()
fig3.subplots_adjust(hspace=0.08)

axs[0].plot(Resultarray.SoC)
axs[0].set_ylabel('SoC')
axs[0].grid(True)



axs[1].plot(Resultarray.Power_updated, label="updated")
axs[1].plot(Resultarray.Power_sim_input,label="root")
axs[1].set_ylabel('Power [kW]')
axs[1].legend()
axs[1].grid(True)

   
axs[2].plot(Resultarray.OCV_Voltage,label="OCV")
axs[2].plot(Resultarray.V_Bat,label="V_Bat")
axs[2].set_ylabel('Voltage Bat')
axs[2].legend()
axs[2].grid(True)






fig4, axs = plt.subplots(3, 1, sharex=True)
    
fig4.tight_layout()
fig4.subplots_adjust(hspace=0.08)

axs[0].plot(Resultarray.SoH_cyc,label="Cyc")
axs[0].plot(Resultarray.SoH_cal,label="Cal")
axs[0].plot(Resultarray.SoH_tot,label="tot")
axs[0].set_ylabel('SoH')
axs[0].legend()
axs[0].grid(True)


'''
axs[1].plot(Results.deg_results.Sum_Deg, label="Sum_deg")
#axs[1].plot(Resultarray.Power_sim_input,label="root")
axs[1].set_ylabel('Power [kW]')
axs[1].legend()
axs[1].grid(True)

   
axs[2].plot(Resultarray.OCV_Voltage,label="OCV")
axs[2].plot(Resultarray.V_Bat,label="V_Bat")
axs[2].set_ylabel('Voltage Bat')
axs[2].legend()
'''

plt.show()






