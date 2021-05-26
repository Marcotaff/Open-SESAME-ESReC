# -*- coding: utf-8 -*-
"""
Created on Mon May 24 17:02:29 2021

@author: blm8
"""

class Cell():
    
    def __init__(self,initial_SoC,initial_Temp,Initial_SoR,inital_SoH,initial_Capacity,SoC_max,SoC_min,lim_Mode,Unom):
        
        self.SoC=initial_SoC
        self.Temp=initial_Temp
        self.SoR=Initial_SoR
        
        self.Vinst=0
        
        self.act_Resistance=0
        
        
        self.limCheckV=False
        self.limCheckSoC=False
        
        self.Capacity=initial_Capacity
        
        self.Cmax=SoC_max*initial_Capacity
        self.Cmin=SoC_min*initial_Capacity
        self.Unom=Unom
        
        self.SoC_max=SoC_max
        self.SoC_min=SoC_min
        
        
        self.deltaC=0
        self.deltaClost=0
        self.updated_current=0
        
        #behavior when a limit is reached
        #Mode1=reject requested Power
        #Mode2=calculate highest possible Current 
        self.lim_Mode=lim_Mode
        
        
   
    def CheckV(self,Resistance,Current,OCVoltage,Vmax,Vmin):
        
        
        self.act_Resistance=self.SoR*Resistance
        
        
        #Voltage Calcultation 
        self.Vinst=OCVoltage+(self.act_Resistance*Current)
        
      
        #Upper Limit Voltage Check 
        if self.Vinst > Vmax:
            
            self.limCheckV=True
            
        else:
            self.limCheckV=False
            
        #Lower Limit Voltage Check 
        if self.Vinst <Vmin:
            
            self.limCheckV=True
            limitside=1
        
        else:
            self.limCheckV=False
            limitside=2
        
        #Update Current 
        if self.limCheckV == True:
            #Mode1
            if self.lim_Mode ==1:
                self.updated_current=0
            
            #Mode 2     
            if self.lim_Mode ==2:
                
                #discharge mode 
                if limitside ==1:
                    self.updated_current=(Vmin-OCVoltage)/self.act_Resistance
                
                #Charge mode
                if limitside ==2:
                    self.updated_current=(Vmax-OCVoltage)/self.act_Resistance
        else:
            self.updated_current = Current   
            
        return
    

    def CalSoC(self,Current,deltaT):

        #Energy of current step 
        self.deltaC=Current*deltaT*self.Unom
        
        #Energy lost over Resistance (current step)
        self.deltaClost=Current*deltaT*self.act_Resistance
        
        #Energy of timestep
        deltaCtot=self.deltaC+self.deltaClost
        
        #Update SoC
        self.SoC=self.SoC+deltaCtot/self.Capacity
        
    
        #Check SoC boundries
        if self.SoC > self.SoC_max:
            
            self.limCheckSoC=True
            limitside=1
        else:
            self.limCheckSoC=False
                
        if self.SoC < self.SoC_min:   
            limitside=2
            self.limCheckSoC=True  
        else:
            self.limCheckSoC=False
            
            
        #Recalculation when SoC limits are reached
        if self.limCheckSoC == True: 
            if self.lim_Mode ==1:  
                
                #Reverse SoC calculation 
                self.SoC=self.SoC-deltaCtot/self.Capacity
            
            if self.lim_Mode ==2: 
                #Charge Mode limit
                if limitside ==1:
                    #get old SoC
                    self.SoC=self.SoC-deltaCtot/self.Capacity 
                    #delta SoC
                    deltaSoC=self.SoC_max-self.SoC
                    deltaC=deltaSoC*self.Capacity
                
                    #Recalculate Current
                    self.updated_current=deltaC/(deltaT*self.Unom+deltaT*self.act_Resistance)
                    
                #Discharge Mode limit 
                if limitside ==2:
                    #get old SoC
                    self.SoC=self.SoC-deltaCtot/self.Capacity 
                    #delta SoC
                    deltaSoC=self.SoC_min-self.SoC
                    deltaC=deltaSoC*self.Capacity
                
                    #Recalculate Current
                    self.updated_current=deltaC/(deltaT*self.Unom+deltaT*self.act_Resistance)
                 
            else:
                self.updated_current=Current
            
        return              
   









    
        

            
                        
            
            
            
            
        
        
    
    