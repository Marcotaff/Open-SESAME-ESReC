
from abc import ABCMeta, abstractmethod

class chemicallibrary:
    __metaclass__=ABCMeta

    @abstractmethod
    def ReadOCVcurve(self):
        pass

    @abstractmethod
    def ReadRcurve(self):
        pass

    @abstractmethod
    def ReadReferenceDr(self):
        pass

    @abstractmethod
    def GetVmax(self):
        pass

    @abstractmethod
    def GetVmin(self):
        pass

    @abstractmethod
    def OCVfromSoC(self):
        pass

    @abstractmethod
    def RfromTempSoC(self):
        pass

    @abstractmethod
    def SF_CalSoC(self):
        pass

    @abstractmethod
    def SF_CalTemp(self):
        pass

    @abstractmethod
    def SF_CycAvgSoc(self):
        pass

    @abstractmethod
    def SF_CycTemp(self):
        pass

    @abstractmethod
    def SF_CycDod(self):
        pass

    @abstractmethod
    def SF_CycCrate(self):
        pass

    @abstractmethod
    def SF_SorAvgSoc(self):
        pass

    @abstractmethod
    def SF_SorDoD(self):
        pass

    @abstractmethod
    def SF_SorCrate(self):
        pass







