import pandas as pd

from simulation_input import simulation_input
from simulation_output import simulation_output

import simulation_parameter
import sim_engine_function

import matplotlib.pyplot as plt


plt.close('all')

#default_params = simulation_parameter.get_simulation_parameter(nominal_energy=100)
own_params = simulation_parameter.get_simulation_parameter(nominal_energy=160,initial_SoC=0.55, SoC_max=1, SoC_min=0, SoH_repeatsim=0.01)

#Define a input objet 
data = simulation_input()
data.read_csv('test_inputdata3.csv')       #read a an input object as csv



#output=sim_engine_function.quick_simulation(data,own_params)
Sim_Results=simulation_output(sim_engine_function.quick_simulation(data,own_params))

#Sim_Results.SoC_plt()
Res1=Sim_Results.iteration_results(own_params.initial_SoH,own_params.initial_SoR)


own_params = simulation_parameter.get_simulation_parameter(nominal_energy=160,initial_SoC=0.55, SoC_max=1, SoC_min=0, SoH_repeatsim=0)
Sim_Results=simulation_output(sim_engine_function.quick_simulation(data,own_params))
Res2=Sim_Results.iteration_results(own_params.initial_SoH,own_params.initial_SoR)


delta=round(abs(Res2.SoH.iloc[-1]-Res1.SoH.iloc[-1]),2)
print("Abweichung",delta)


fig2, axs = plt.subplots()
axs.scatter(Res1.calculation_iteration,Res1.SoH,label="Saprox_Sim")
axs.plot(Res2.calculation_iteration,Res2.SoH,label="full_sim")
axs.grid(True)
axs.set_ylabel('SoH')
axs.set_xlabel('Number of Iterations')
axs.set_title('SOH calc deviation '+str(round(delta*100,2))+'%SoH')
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



019
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

