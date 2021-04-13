# Open-SESAME-ESReC
Battery model 
This folder contains most of the required files for running the code.
1. main.py: This is the code which reads the parameters and csv files, calls a function for the calculation of the degradation and outputs the results.
2. cycling.py: This is the code where the computation of the degradation of the cell takes place.
3. NMC.py: This is a function package which contains the stress factor dependencies for the NMC chemistry. This is called by cycling.py when the cell chemistry is NMC.
4. csv files: This is a folder which contains various csv files. 
  i. sample temperature profile.csv: This file contains the daily average temperature data, which is used to assign the temperature of the cell in the model
  ii. NMC SOC-OCV 2.csv: This csv file contains the data for the soc-ocv curve. It contains the voltage at 1% SoC steps from 0% SoC to 100% SoC in the increasing order.
  iii. r-soc-temp (extensive,1Hz).csv: This csv file contains the extrapolated values of the resistance of the cell at different conditions using the code above (sr. no. 5)
5. input parameters.xlsx: This excel files acts as a GUI which the user can enter various battery parameters such as the battery size, number of days to be simulated, cell chemistry as so on.
