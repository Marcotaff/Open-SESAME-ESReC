#todo: open sesame header with copyright information, GNU License, whatever



import numpy as np
import pandas as pd



#this class defines a simulation input object
class simulation_input():
    def __init__(self):            
        #set up some dummy arrays   
        self.power_W = np.zeros(1)                  #current vector in Amps. Charge current positive, discharge negative
        self.ambient_temperature_C = np.zeros(1)      #ambient temperature vector in °C

    #get data as pandas data frame with time vector as index
    def get_as_dataframe(self):    
        data = {'power_W':            self.power_W.tolist(),
                'ambient_temperature_C': self.ambient_temperature_C.tolist()
            }
        df = pd.DataFrame(data) 
        return df

    #overwrites internal numpy values with data from pandas dataframe, expects time as index
    def restore_from_dataframe(self, inputframe): 
        self.power_W = np.array(inputframe['power_W'].tolist())                
        self.ambient_temperature_C = np.array(inputframe['ambient_temperature_C'].tolist())    

    #writes data to a csv file
    def write_csv(self, filename, separator=','):
        df = self.get_as_dataframe()
        df.to_csv(filename, sep=separator)

    
    #reads data from a csv file
    def read_csv(self, filename, separator=','):
        df=pd.read_csv(filename, sep=separator)  
        self.restore_from_dataframe(df)

    
    #provides some statistical key values to check if the data correspond to the expectations
    def describe(self): 
        df = self.get_as_dataframe()
        return df.describe()
           

        
   
