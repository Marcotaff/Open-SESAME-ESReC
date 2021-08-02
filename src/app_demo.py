import pandas as pd

from simulation_input import simulation_input
from simulation_output import simulation_output

import simulation_parameter
import sim_engine_function

import matplotlib.pyplot as plt


plt.close('all')

#default_params = simulation_parameter.get_simulation_parameter(nominal_energy=100)


#Define a input objet 
data = simulation_input()
data.read_csv('test_inputdata3.csv')       #read a an input object as csv





own_params = simulation_parameter.get_simulation_parameter(nominal_energy=160,initial_SoC=0.55, SoC_max=1, SoC_min=0, SoH_repeatsim=0)
Sim_Results=simulation_output(sim_engine_function.simulation(data,own_params))
Res2=Sim_Results.iteration_results(own_params.initial_SoH,own_params.initial_SoR)
Sim_Results.SoH_plt(Res2)
data.power_W=data.power_W*1000



own_params = simulation_parameter.get_simulation_parameter(nominal_energy=160,initial_SoC=0.55, SoC_max=1, SoC_min=0, SoH_repeatsim=0.02)
Sim_Results=simulation_output(sim_engine_function.simulation(data,own_params))
Res3=Sim_Results.iteration_results(own_params.initial_SoH,own_params.initial_SoR)
data.power_W=data.power_W*1000

own_params = simulation_parameter.get_simulation_parameter(nominal_energy=160,initial_SoC=0.55, SoC_max=1, SoC_min=0, SoH_repeatsim=0.01)
Sim_Results=simulation_output(sim_engine_function.simulation(data,own_params))
Res1=Sim_Results.iteration_results(own_params.initial_SoH,own_params.initial_SoR)
data.power_W=data.power_W*1000





fig2, axs = plt.subplots()
axs.plot(Res1.calculation_iteration,Res1.SoH,'o--',label="Aprox. Simulation with delta SoH 1%")
axs.plot(Res3.calculation_iteration,Res3.SoH,'o--',label="Aprox. Simulation with delta SoH 2%")
axs.plot(Res2.calculation_iteration,Res2.SoH,'o--',label="Full Simulation")


axs.set_ylabel('SoH')
axs.set_xlabel('Number of Iterations')
axs.grid(True)
axs.set_title('Results of three different Simulations')
plt.legend()


plt.legend()
plt.show()




'''
#this way 
#Results=simulation_output(sim_engine_function.simulation(data,own_params))

Results=simulation_output(sim_engine_function.quick_simulation(data,own_params))


Resultarray=Results.get_def_resultarray(own_params.initial_SoH,own_params.initial_SoH)
Results.write_def_csv("outputtest.csv", separator=',')


#Testplots


fig1, axs = plt.subplots(3, 1, sharex=True)
    
fig1.tight_layout()
fig1.subplots_adjust(hspace=0.08)

axs[0].plot(Resultarray.SoC)
axs[0].set_ylabel('SoC')
axs[0].grid(True)




axs[1].plot(Resultarray.Power_updated, label="updated")
axs[1].plot(Resultarray.Power_sim_input,label="root")
axs[1].set_ylabel('Power [kW]')
axs[1].legend(loc='upper right')
axs[1].grid(True)

   
axs[2].plot(Resultarray.OCV_Voltage,label="OCV")
axs[2].plot(Resultarray.V_Bat,label="V_Bat")
axs[2].set_ylabel('Voltage Bat')
axs[2].legend(loc='upper right')
axs[2].grid(True)






fig2, axs = plt.subplots(3, 1, sharex=True)
    
fig2.tight_layout()
fig2.subplots_adjust(hspace=0.08)

axs[0].plot(Resultarray.SoH_cyc,label="SoH_Cyc")
axs[0].plot(Resultarray.SoH_cal,label="SoH_Cal")
axs[0].plot(Resultarray.SoH_tot,label="SoH_tot")
axs[0].plot(Resultarray.SoH_feedback,label="feedback SoH")
axs[0].set_ylabel('SoH')
axs[0].legend(loc='upper right')
axs[0].grid(True)



axs[1].plot(Resultarray.SoR_tot, label="SoR")
axs[1].plot(Resultarray.SoR_feedback,label="feedback")
axs[1].set_ylabel('SoR')
axs[1].legend()
axs[1].grid(True)

   
axs[2].plot(Resultarray.Resistance,label="Resistance")
axs[2].set_ylabel('Resistance')
axs[2].legend()


plt.show()
'''




