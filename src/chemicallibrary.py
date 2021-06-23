
from abc import ABC, abstractmethod

class chemicallibrary(ABC):
    

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def OCVfromSoC(self):
        pass

    @abstractmethod
    def RfromTempSoC(self):
        pass

    @abstractmethod
    def Imp_CalSoC(self):
        pass

    @abstractmethod
    def Imp_CalTemp(self):
        pass

    @abstractmethod
    def Imp_CycAvgSoc(self):
        pass

    @abstractmethod
    def Imp_CycTemp(self):
        pass

    @abstractmethod
    def SF_CycDod(self):
        pass

    @abstractmethod
    def SF_CycCrate(self):
        pass

    @abstractmethod
    def Imp_SorAvgSoc(self):
        pass

    @abstractmethod
    def Imp_SorDoD(self):
        pass

    @abstractmethod
    def SF_SorCrate(self):
        pass







