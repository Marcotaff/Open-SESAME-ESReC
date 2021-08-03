
from abc import ABC, abstractmethod

class chemicallibrary(ABC):
    

    @abstractmethod
    def __init__(self):
        pass
    
    @abstractmethod
    def operational_range_check(self):
        pass
    
    #Performance related Functions 
    @abstractmethod
    def OCVfromSoC(self):
        pass

    @abstractmethod
    def RfromTempSoC(self):
        pass

     #Calendaric Stressfactors SOH
    @abstractmethod
    def Imp_CalSoC(self):
        pass

    @abstractmethod
    def Imp_CalTemp(self):
        pass

    # Cyclic Stressfactors SOH 
    @abstractmethod
    def Imp_CycAvgSoc(self):
        pass

    @abstractmethod
    def Imp_CycTemp(self):
        pass

    @abstractmethod
    def Imp_CycDod(self):
        pass

    @abstractmethod
    def Imp_CycCrate(self):
        pass
    
    #SoR Cyclic Stressfactors 
    @abstractmethod
    def Imp_SorAvgSoc(self):
        pass

    @abstractmethod
    def Imp_SorDoD(self):
        pass

    @abstractmethod
    def Imp_SorCrate(self):
        pass
    
    @abstractmethod
    def Imp_SorTemp(self):
        pass
    
    #SoR Calendaric stressfactors 
    @abstractmethod
    def Imp_SorCalSoC(self):
        pass
    
    @abstractmethod
    def Imp_SorCalTemp(self):
        pass







