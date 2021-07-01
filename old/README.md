# Open-SESAME-ESReC
Battery model 
This folder contains most of the required files for running the code.
1. Code.py: This is the code to compute the amount of battery degradation after a given profile is executed.
2. geneva temp data.csv: This file contains the daily average temperature data for geneva, which is used to assign the temperature of the cell in the model
3. NMC SOC-OCV 2.csv: This csv file contains the data for the soc-ocv curve. It contains the voltage at 1% SoC steps from 0% SoC to 100% SoC in the increasing order.
4. ocv-soc extraction.py: This is the code used to extract the values for the soc-ocv curve (sr. no. 3)
5. r_soc_temp_map.m: This is the matlab code used to extrapolate the resistance of the cell at different soc and temperature conditions given the resistance at a few of the conditions.
6. r-soc-temp (extensive,1Hz).csv: This csv file contains the extrapolated values of the resistance of the cell at different conditions using the code above (sr. no. 5)
7. Sample GITT.csv: This csv file contains the data that is taken as an input in the ocv-soc extraction code (sr. no. 4)
8. SoH/SoR SF parameterization: These excel files show the methodology followed to derive the dependence of the stress factors on the various parameteres, which are then used to develop the degradation model
