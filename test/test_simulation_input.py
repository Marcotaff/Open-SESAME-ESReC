import unittest
import numpy as np

from src.simulation_input import simulation_input

class test_simulation_input(unittest.TestCase):
    #setup() runs before the test and is often used to prepare a common environment used in multiple test
    def setUp(self):
        self.testinput = simulation_input()     #creates a new object available for testing    
        self.add_dummy_data(self.testinput)     #prepare a dummy input vector to be used in the tests
    
    #adds some dummy data to the provided destination
    def add_dummy_data(self, dest, size=100):
        dest.power_W = np.random.rand(size)               
        dest.ambient_temperature_C = np.ones(size) * 25
    
    def test_setup(self):
        #make sure we do not have an empty testinput
        self.assertGreater(len(self.testinput.power_W * 100),1)
        self.assertGreater(len(self.testinput.ambient_temperature_C),1)
        
    def test_csv(self):
        self.testinput.write_csv('temp.csv')
        
        new_input = simulation_input() 
        new_input.read_csv('temp.csv')

        #check that new_input has same data as self.testinput 
        self.assertTrue(np.allclose(self.testinput.power_W, new_input.power_W))
        self.assertTrue(np.allclose(self.testinput.ambient_temperature_C,new_input.ambient_temperature_C))
        
   
        
