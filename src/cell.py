# -*- coding: utf-8 -*-
"""
Created on Mon May 24 17:02:29 2021

@author: blm8
"""

class Cell():
    
    def __init__(self,initial_SoC,initial_Temp,Initial_SoR,initial_SoH,initial_Capacity,lim_Mode,initial_Q):
        
        self.SoC=initial_SoC        #SoC of the battery gets updated in method CalSoC
        self.Temp=initial_Temp      #Temperature of the battery must be updated externaly
        self.SoR=Initial_SoR        #state of health of the Resistance must be updated externaly 
        self.SoH=initial_SoH        #State of health of the battery (Capacity) must be updated externaly 
        
        
        self.Vinst=0                #Current Voltage at the Cellpoles
        self.act_Resistance=0       #Resitance at current operating condition 
        
        
        self.limCheckV=False        #Variable contains information if a Voltage limit is reached 
        self.limCheckSoC=False      #Variable contains information if a SoC limit is reached 
       
        
       
        self.Q=initial_Q                    #electric Charge of battery in Ah
        self.Capacity=initial_Capacity      #Battery Capacity in kWh
        self.Q_ini = initial_Q               # initial electric charge of battery in Ah
        self.Capacity_ini = initial_Capacity    # initial battery charge in kWh

    
        self.deltaC=0           #usable or used Energy of timestep   
        self.updated_current=0  #Current of the timestep 
        
        self.act_Energy = self.SoC*self.Capacity
        self.act_Q = self.SoC*self.Q
        
        #behavior when a limit is reached
        #Mode1=reject requested Power
        #Mode2=calculate highest possible Current 
        self.lim_Mode=lim_Mode
        
        if self.lim_Mode != 1 and self.lim_Mode != 2:
            self.lim_Mode=2
    
     
        self.Crate =0
        self.Power_upd=0
        
        
        
        
   #Check if the Voltage limites are reached under the current conditions
   #Adjust or reject the requested Power 
    def CheckV(self,Resistance,Power,OCVoltage,Vmax,Vmin):
        
        '''
        Inputs:
            -Resistance[Ohm], (Will be multiplied by the SoR)
            -Power [kW], requested Power from the aplication (positiv = charging, negativ =discharge) 
            -OCVoltage [V], Open circuit Voltage 
            -Vmax [V], maximum allowed Voltage of Cell
            -Vmin [V], minimal allowed Voltage of Cell 
        '''
        #Calculate the Crate
        self.Crate=Power/self.Capacity
        
        #Calculate the Current 
        self.updated_current=self.Crate*self.Q
        
        #Calculate the Resistance 
        self.act_Resistance=self.SoR*Resistance
        
        #Voltage Calcultation 
        self.Vinst=OCVoltage+(self.act_Resistance*self.updated_current)
        
        self.limCheckV=False
        #Upper Limit Voltage Check 
        if self.Vinst > Vmax:
         
            self.limCheckV=True
            limitside=2
        
        #Lower Limit Voltage Check 
        if self.Vinst <Vmin:
       
            self.limCheckV=True
            limitside=1
    
        #Update Current 
        if self.limCheckV == True:
            #Mode1
            if self.lim_Mode ==1:
                self.updated_current=0
                self.Vinst=OCVoltage
            
            #Mode 2     
            if self.lim_Mode ==2:
                
                #discharge mode 
                if limitside ==1:
                    self.updated_current=(Vmin-OCVoltage)/self.act_Resistance
                    self.Vinst=Vmin
                
                #Charge mode
                if limitside ==2:
                    self.updated_current=(Vmax-OCVoltage)/self.act_Resistance
                    self.Vinst=Vmax
        else:
            #Update Current 
            self.updated_current = self.updated_current
        
        #Crate update 
        self.Crate=self.updated_current/self.Q
        self.Power_upd=self.Crate*self.Capacity
        
    
        return
    

    def CalSoC(self,Power,deltaT,SoC_max,SoC_min):

   

        '''
        Inputs:
            -Power [kW], requested Power from the aplication (positiv = charging, negativ =discharge) 
            -deltaT [Sec], timestep between measurements 
        '''
        self.SoC_max=SoC_max 
        self.SoC_min=SoC_min
        
        
        deltaT=deltaT/(60*60) #in hours 
        
        #Calculate the C-Rate 
        self.Crate=Power/self.Capacity
        
        #Calculate the Power 
        self.updated_current=self.Crate*self.Q
        
        #Energy of current step 
        self.deltaC=self.updated_current*deltaT
        
        
        #Update SoC
        self.SoC=self.SoC+self.deltaC/self.Q
        
        
        self.limCheckSoC=False
        
        #Check SoC boundries
        if self.SoC > self.SoC_max:
            
            self.limCheckSoC=True
            limitside=1
            
                
        if self.SoC < self.SoC_min:   
            limitside=2
            self.limCheckSoC=True  
        
        #Recalculation when SoC limits are reached
        if self.limCheckSoC == True: 
            if self.lim_Mode ==1:  
                
                #Reverse SoC calculation 
                self.SoC=self.SoC-self.deltaC/self.Q
                self.Crate=0
                self.updated_current=0
                self.deltaC=0
                self.deltaClost=0
                 
            
            if self.lim_Mode ==2: 
               
                self.deltaSoC=0
                #Charge Mode limit
                if limitside ==1:
                    #get old SoC
                    self.SoC=self.SoC-self.deltaC/self.Q
                    #delta SoC
                    self.deltaSoC=self.SoC_max-self.SoC
                    self.SoC=self.SoC_max
                    
        
                #Discharge Mode limit 
                if limitside ==2:
                    #get old SoC
                    self.SoC=self.SoC-self.deltaC/self.Q
                    #delta SoC
                    self.deltaSoC=self.SoC_min-self.SoC
                    self.SoC=self.SoC_min
              
                #Recalculate 
                self.deltaC=self.deltaSoC*self.Q
                self.updated_current=self.deltaC/deltaT
                self.Crate=self.updated_current/self.Q
              
                self.Power_upd=self.Crate*self.Capacity
                
        self.act_Energy = self.SoC*self.Capacity
        self.act_Q = self.SoC*self.Q    

        return
    
    
    def update(self,delta_SoH,delta_SoR):
        
        
        self.SoH=self.SoH-delta_SoH
        
        self.SoR=self.SoR+delta_SoR
        
        #Update the Energy and the Capcacity 
        
        self.Capacity=self.Capacity_ini*self.SoH
        self.Q=self.Q_ini*self.SoH
        
        
        
        return 
    
    