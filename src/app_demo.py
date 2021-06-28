import pandas as pd

from simulation_input import simulation_input
from simulation_output import simulation_output

import simulation_parameter
import sim_engine_function

import matplotlib.pyplot as plt




default_params = simulation_parameter.get_simulation_parameter(nominal_energy=100)
own_params = simulation_parameter.get_simulation_parameter(nominal_energy=100,initial_SoC=0.5, SoC_max=1, SoC_min=0)


data = simulation_input()
data.read_csv('test2.csv')       #read a an input object as csv



#for shubham:
#data = myOwnInputManager()   #your fucntion should return a simulation_input object 

#output1 = sim_engine_function.simulation(data, default_params)
#output2 = sim_engine_function.simulation(data, own_params)


#this way 
Results=simulation_output(sim_engine_function.simulation(data,own_params))




Resultarray=Results.get_def_resultarray()
Results.write_def_csv("outputtest.csv", separator=',')






fig=plt.subplot()

plt.plot(Resultarray.SoH)

plt.show()






