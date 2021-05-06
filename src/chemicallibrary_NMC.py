
from abc import ABCMeta, abstractmethod
import chemicallibrary


class chemicallibrary_NMC(chemicallibrary):

    def ReadOCVcurve(self):
        pass

    def ReadRcurve(self):
        pass

    def ReadReferenceDr(self):
        pass


    def GetVmax(self):
        pass


    def GetVmin(self):
        pass


    def OCVfromSoC(self):
        pass


    def RfromTempSoC(self):
        pass


    def SF_CalSoC(self):
        pass


    def SF_CalTemp(self):
        pass


    def SF_CycAvgSoc(self):
        pass


    def SF_CycTemp(self):
        pass


    def SF_CycDod(self):
        pass


    def SF_CycCrate(self):
        pass


    def SF_SorAvgSoc(self):
        pass


    def SF_SorDoD(self):
        pass


    def SF_SorCrate(self):
        pass

