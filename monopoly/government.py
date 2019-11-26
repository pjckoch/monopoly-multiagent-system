import random
import numpy as np
from enum import Enum
import data_manager
import helper_funs
import logger

prevPol = 0

class Government():
    """An intelligent agent that interacts with other agents in order to regulate the happiness."""

    # Government Politics can be LIBERAL, NEUTRAL or COMMUNIST

    def __init__(self,
                 politics="LIBERAL",
                 taxesStatus=None,
                 subsidiariesStatus=None,
                 taxRate=0.1,
                 subsidyValue=50,
                 governmentMoney=0,
                 startCompPrice=9000,
                 investOwnCompPrice=3000):
        self.politics = PoliticsSwitcher.LIBERAL if politics is None else politics
        self.taxesStatus = [] if taxesStatus is None else taxesStatus
        self.subsidiariesStatus = [] if subsidiariesStatus is None else subsidiariesStatus
        self.taxRate = taxRate
        self.subsidyValue = subsidyValue
        self.governmentMoney = governmentMoney
        self.startCompPrice = startCompPrice
        self.investOwnCompPrice = investOwnCompPrice

    def startAuction(self, companyId):
        return None

    def isPersonHelped(self, bm):
        for subs in self.subsidiariesStatus:
            if subs[0] == bm.id:
                return True
        return False

    def sortListByCapital(self, bmList):
        tempBmList = bmList.copy()
        sortedList = []
        minCapital = 99999
        minBm = None

        while len(tempBmList) != 0:
            for bm in tempBmList:
                if bm.capital < minCapital:
                    minCapital = bm.capital
                    minBm = bm
            tempBmList.remove(minBm)
            sortedList.append(minBm)
            minCapital = 99999
            minBm = None

        return sortedList

    # Returns the percentage of government money for subsidiaries that a bm will receive
    def calculateSubsidiaryPercentage(self, index, bmList):
        inverseList = bmList[::-1]
    
        totalBmMoney = 0
        for bm in bmList:
            totalBmMoney += bm.capital

        return inverseList[index].capital/totalBmMoney

    def calculateSubsidiaryFormula(self, capital):
        val = 3000
        # if self.politics == "LIBERAL":
        #     val = 3000
        # elif self.politics == "NEUTRAL":
        #     val = 5000
        # elif self.politics == "COMMUNIST":
        #     val = 3000
        if capital + 1 < 0: # to avoid encountering log(0) error
            capital = 0
        return val-100*np.log(capital+1)

    # Give Equal Subsidiaries to Everyone
    def calculateSubsidiary(self, bm, govMon, noBm):
        return govMon/len(bmList)

    # Give Differentiated Subsidiaries to Everyone
    def calculateSubsidiaryOnSteroids(self, bm, govMon, bmList):
        sortedList = self.sortListByCapital(bmList)
        index = sortedList.index(bm)
        return govMon * self.calculateSubsidiaryPercentage(index, bmList)

    # Give Differentiated Subsidiaries to Poor People When They are Below 2000$
    def robinHoodMode(self, bm):
        val = 4000
        if self.politics == "LIBERAL":
            val = 3000
        elif self.politics == "NEUTRAL":
            val = 4000
        elif self.politics == "COMMUNIST":
            val = 5000
        if bm.capital < val:
            return self.calculateSubsidiaryFormula(bm.capital)
        return 0


    def regulateSubsidiary(self,businessman,govMon, bmList):
        subs = self.robinHoodMode(businessman)
        if self.governmentMoney - subs > 0:
            businessman.subsidiariesHistory.append(subs)
            helper_funs.transaction(self, businessman, subs)

    def regulateTax(self,bm, company, time):
        company.taxHistory.append(company.bruttoProfitHistory[-1] * self.taxRate)
        helper_funs.transaction(company, self, company.taxHistory[-1])


    def regulate(self, businessmenList):
        momentaryGovMoney = self.governmentMoney
        for bm in businessmenList:
            self.regulateSubsidiary(bm, momentaryGovMoney, len(businessmenList))


class PoliticsSwitcher(Enum):

    """Defines the economical strategy of the government"""
    LIBERAL = 1
    NEUTRAL = 0
    COMMUNIST = -1