#todo: open sesame header with copyright information, GNU License, whatever



import numpy as np
import pandas as pd



#this class defines a simulation input object
class simulation_input():
    def __init__(self):            
        #set up some dummy arrays   
        self.time_hours = np.zeros(1)                 #time vector in hours
        self.current_A = np.zeros(1)                  #current vector in Amps. Charge current positive, discharge negative
        self.ambient_temperature_C = np.zeros(1)      #ambient temperature vector in °C
        self.data_size = 1                            #number of days worth of data in csv file (days)
        self.data_resolution = 1                      #resolution of data in csv file (seconds)

    #get data as pandas data frame with time vector as index
    def get_as_dataframe(self):    
        data = {'time_hours': self.time_hours.tolist(),
                'current_A':  self.current_A.tolist(),
                'ambient_temperature_C': self.ambient_temperature_C.tolist()
            }
        df = pd.DataFrame(data, columns = ['time_hours', 'current_A','ambient_temperature_C'])
        return df.set_index('time_hours')

    #overwrites internal numpy values with data from pandas dataframe, expects time as index
    def restore_from_dataframe(self, inputframe):
        self.time_hours = np.array(inputframe.index)  
        self.current_A = np.array(inputframe['current_A'].tolist())                
        self.ambient_temperature_C = np.array(inputframe['ambient_temperature_C'].tolist())    

    #writes data to a csv file
    def write_csv(self, filename, separator=','):
        df = self.get_as_dataframe()
        df.to_csv(filename, sep=separator)

    
    #reads data from a csv file
    def read_csv(self, filename, separator=','):
        df=pd.read_csv(filename, sep=separator, index_col='time_hours')  
        self.restore_from_dataframe(df)

    
    #provides some statistical key values to check if the data correspond to the expectations
    def describe(self): 
        df = self.get_as_dataframe()
        print(df.describe())
           

    #returns true if the data is consistent 
    #i guess this one better goes into the simulation part to check input vectors before running simulation
    def consistency_check(self):
        #time should be constantly increasing
        #same length for all vectors
        #length bigger than one
        return False  #todo: implement
