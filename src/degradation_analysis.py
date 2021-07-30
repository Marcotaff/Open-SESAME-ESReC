# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 08:57:23 2021

@author: blm8
"""

from cyc_counting_algorithm import  Rainflow_mod,PeaktoPeak  
import pandas as pd 
import numpy as np
from math import sin, cos

from chemicallibrary_NMC import chemicallibrary_NMC


class degradation():
    
    def  __init__(self, Cell_chemistry,timeresolution,cyc_counting_alg):

        
        self.timeresolution=timeresolution
        
        if Cell_chemistry=="NMC":
            self.Chemistry_obj=chemicallibrary_NMC()  
        
        #if Cell_chemistry=="LTO":
            #self.Chemistry_obj=chemicallibrary_LTO()
            
        self.delta_SoH=0
        self.delta_SoR=0
        
        self.cyc_counting_alg=cyc_counting_alg
        
        if self.cyc_counting_alg != 1 or self.cyc_counting_alg != 2:
            self.cyc_counting_alg =1


    def compute(self,SoC_prof,Crate_prof,Temp_prof,startindex_fragment):
        
        '''
        Inputs:
            -SoC_prof    numpy series
            -Crate_prof  numpy series 
            -Temp_prof   numpy series 

        Outputs:
            -Cyc_Results Results of Cycle counting alg  pandas df
            Con_Results  Degradation results for every timestep  pandas df 
        '''
        
        #___________________________________________________________________________
        #Apply Cylce Counting algorithm 
        
        if  self.cyc_counting_alg==1:
            Cycle_results=Rainflow_mod(SoC_prof,Crate_prof,Temp_prof)
        
        if  self.cyc_counting_alg==2: 
            Cycle_results=PeaktoPeak(SoC_prof,Crate_prof,Temp_prof)
        

        if len(Cycle_results) ==1:
            if Cycle_results[0,5]==0:
                
                Cycle_results[0,:]=0
         
       
        #___________________________________________________________________________
        #Create Result arrays
    
        leng=len(Cycle_results)
        deg_results=np.zeros((leng,19))
        
        leng=len(SoC_prof)
        con_deg_results=np.zeros((leng,10))
    
        #___________________________________________________________________________
        #Calc SF for every Cycle found 
        for c in range(0,len(Cycle_results)):
       
            #Half/fullcycles
            cycle_equivalent=Cycle_results[c,1]*Cycle_results[c,0] #changed!!!!!!!!!!!
       
            #--------------------------------------------
            # Cycle related stress factors (SF)
            
            #Get Cycle values 
            DoD=Cycle_results[c,0]
            Crate=Cycle_results[c,5]
            AVG_Temp=Cycle_results[c,7]
            AVG_SoC=Cycle_results[c,4]
            
            #Compute Stressfactors 
            SF_DoD=self.Chemistry_obj.Imp_CycDod(DoD)
            SF_Crate=self.Chemistry_obj.Imp_CycCrate(Crate)
            Imp_AVGSoC=self.Chemistry_obj.Imp_CycAvgSoc(AVG_SoC)
            Imp_Temp=self.Chemistry_obj.Imp_CycTemp(AVG_Temp)
            
            #Sum Stressfactors up 
            SF_cyclic_sum= SF_DoD*SF_Crate*Imp_AVGSoC*Imp_Temp*cycle_equivalent
            Tot_Soh_cyc=self.Chemistry_obj.refCyc*SF_cyclic_sum
            
            #--------------------------------------------
            #SoR related stress factors (SF)
            
            
            R_SF_Dod=self.Chemistry_obj.Imp_SorDoD(DoD)
            R_SF_Crate=self.Chemistry_obj.Imp_SorCrate(Crate)
            R_SF_AVGSoC=self.Chemistry_obj.Imp_SorAvgSoc(AVG_SoC)
            R_SoR_sum= R_SF_Dod*R_SF_Crate*R_SF_AVGSoC*cycle_equivalent
        
            Tot_Sor_cycle=self.Chemistry_obj.refSor*R_SoR_sum
        
            #---------------------------------------------
            #Save SF results for each step
    
            
            deg_results[c,0]=     SF_DoD
            deg_results[c,1]=     SF_Crate
            deg_results[c,2]=     Imp_AVGSoC
            deg_results[c,3]=     Imp_Temp
            deg_results[c,4]=     SF_cyclic_sum
            deg_results[c,5]=     Tot_Soh_cyc 
            
            deg_results[c,6]=     R_SF_Dod 
            deg_results[c,7]=     R_SF_Crate
            deg_results[c,8]=     R_SF_AVGSoC  
            deg_results[c,9]=     R_SoR_sum
            deg_results[c,10]=    Tot_Sor_cycle
            
            
            deg_results[c,11]=    Cycle_results[c,0]
            deg_results[c,12]=    Cycle_results[c,1]
            deg_results[c,13]=    Cycle_results[c,2]
            deg_results[c,14]=    Cycle_results[c,3]
            deg_results[c,15]=    Cycle_results[c,4]
            deg_results[c,16]=    Cycle_results[c,5]
            deg_results[c,17]=    Cycle_results[c,6]
            deg_results[c,18]=    Cycle_results[c,7]
            
      
        #___________________________________________________________________________
        #Calendaric Degradation (for each timestamp)
        
        for x in range(0,len(SoC_prof)):
            
            #SoH Stressfactors 
            SoC=SoC_prof[x]
            SF_Cal_SoC=self.Chemistry_obj.Imp_CalSoC(SoC)
            
            Temp=Temp_prof[x]
            SF_Cal_Temp=self.Chemistry_obj.Imp_CalTemp(Temp)
            
            #Total 
            Tot_cal=SF_Cal_SoC*SF_Cal_Temp*self.Chemistry_obj.refCal*self.timeresolution
            
            #SoR Stressfactors
            
            R_SF_Cal_SoC=1
            R_SF_Cal_Temp=1
            
            R_Tot_cal=1#R_SF_Cal_SoC*R_SF_Cal_Temp*self.Chemistry_obj.refCal*self.timeresolution #######Change needed! 
            
            
            #Save Results 
            con_deg_results[x,0]=     SF_Cal_SoC 
            con_deg_results[x,1]=     SF_Cal_Temp
            con_deg_results[x,2]=     Tot_cal
 
    
            con_deg_results[x,7]=     R_SF_Cal_SoC 
            con_deg_results[x,8]=     R_SF_Cal_Temp
            con_deg_results[x,9]=     R_Tot_cal
            #___________________________________________________________________________
             #Adding cycle results to the continious results 
          
            index=np.asarray(np.where(Cycle_results[:,3]==x))
            first=index[0]
          
            if first.size > 0:
                 index=int(first[0])
                 con_deg_results[x,3]=deg_results[index,5]  #TOT_cyc
                 con_deg_results[x,5]=deg_results[index,10] #TOT SoR 

            else:
                con_deg_results[x,3]=0
                con_deg_results[x,5]=0  #Tot_SoR
         
        #Sum them together 
        con_deg_results[:,4]=con_deg_results[:,3]+con_deg_results[:,2] #Sum Cal and Cyc aging          
        
        con_deg_results[:,6]=con_deg_results[:,5]+con_deg_results[:,9] #Sum Cal and Cyc aging 
      
        #___________________________________________________________________________
        #calculate delta SoH and delta_SoR of fragment  
        
        self.delta_SoH=np.sum(con_deg_results[:,4])/100
        self.delta_SoR=np.sum(con_deg_results[:,5])/100
        
        #___________________________________________________________________________
        #preparing the result array for the output , change to pandas dataframe 
        
        #Updating the Index of cycle Results according to the inputdata as a hole 
        
    
        deg_results[:,2]=deg_results[:,2]+int(startindex_fragment) 
        deg_results[:,3]=deg_results[:,3]+int(startindex_fragment)

        
        return deg_results,con_deg_results
    
    
   
        
        



