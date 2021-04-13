import numpy as np
import pandas as pd
import os
import cycling
import matplotlib.pyplot as plt

# READING FILES FOR INPUT
ip = np.array(pd.read_excel(r'input_parameters.xlsx'))
input_profile = np.array(pd.read_csv(ip[8,1],header=None).values)     # CSV with power for every second of every day of the year/years (each second of the day in a new row, each day in a new column)
temp = np.array(pd.read_csv(ip[9,1],header=None).values)       # CSV file containing daily average temperature data for a whole year in Geneva (in °C)

# FOLDER CREATION TO SAVE DAILY INPUT PROFILES AND FINAL RESULTS
fil_name = ip[7,1]                      # name to the file to which the daily input profiles will be stored
dir_name = os.getcwd()
os.mkdir(dir_name+'\\'+fil_name)        # making folder to save the figures
n = dir_name + '\\' + fil_name + '\\'

# '+' means power from the battery and '-' means power to the battery

# SCENARIO PARAMETERS
days = ip[6,1] # number of days you want to simulate
bsize = ip[0,1]                      # size of the battery in the vehicle (kWh)

# CELL PARAMETERS
cell_chem = ip[10,1]        # cell chemistry to be simulated
soc_min = ip[1,1]           # minimum soc during cycling
soc_max = ip[2,1]           # maximum soc during cycling
v_max = ip[4,1]             # maximum voltage during cycling
v_min = ip[3,1]             # minimum voltage during cycling
soc = soc_in = ip[5,1]      # minimum initial SoC

# CYCLING THE CELL USING THE GIVEN PARAMETERS
Qlcal, Qlcyc, Qlsor, Q_soc_max, Q_soc_min = cycling.deg_calc(cell_chem,bsize,v_min,v_max,soc_min,soc_max,soc_in,days,n,temp,input_profile)
SoH = 100-(Qlcal+Qlcyc)

# PLOTTING THE RESULTS
plt.plot(Qlcal,'r',Qlcyc,'b',Qlcyc+Qlcal,'g')
plt.xlabel('time (days)'); plt.ylabel('Degradation (%)'); plt.legend(['calendar','cycle','total']); plt.savefig(n+'Degradation');
plt.close()
plt.plot(Qlsor)
plt.xlabel('time (days)'); plt.ylabel('SoR (%)'); plt.savefig(n+'SoR');
plt.close()
plt.plot(Q_soc_max,'r',Q_soc_min,'b')
plt.xlabel('time (days)'); plt.ylabel('SoC'); plt.legend(['SoC max','SoC min']); plt.savefig(n+'SoC range');
plt.close()

print('The calendar and cycle aging are '+ str(Qlcal[-1]) + ' and ' + str(Qlcyc[-1]) + ' respectively')
print('The SoR is ' + str(Qlsor[-1]))