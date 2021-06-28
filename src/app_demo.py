import pandas as pd

from simulation_input import simulation_input
import simulation_parameter
import sim_engine_function



default_params = simulation_parameter.get_simulation_parameter(nominal_energy=200)
own_params = simulation_parameter.get_simulation_parameter(nominal_energy=200,initial_SoC=0.8, SoC_max=0.8, SoC_min=0.3)


data = simulation_input()
data.read_csv('test3.csv')       #read a an input object as csv

#for shubham:
#data = myOwnInputManager()   #your fucntion should return a simulation_input object 

output1 = sim_engine_function.simulation(data, default_params)
output2 = sim_engine_function.simulation(data, own_params)

#todo: do something with the output



# def myInputManager():
#     data = simulation_input()
#
#     data.temperature= getfromsomehwere and interpolate
#     
#     parameter = get_simulation_parameter()
#     
#     return data, parameter
    