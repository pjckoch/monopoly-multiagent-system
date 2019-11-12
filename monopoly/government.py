import random
import numpy as np
from enum import Enum
import data_manager


class Government():
    """An intelligent agent that interacts with other agents in order to regulate the happiness."""

    # Government Politics can be supportive, neutral or competitive

    def __init__(self,
                 politics=None,
                 taxesStatus=None,
                 subsidiariesStatus=None,
                 taxRate=0.5,
                 subsidyValue=50,
                 governmentMoney=0,
                 startCompPrice=9000,
                 investOwnCompPrice=3000):
        self.politics = PoliticsSwitcher.SUPPORTIVE if politics is None else politics
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
        if capital + 1 < 0: # to avoid encountering log(0) error
            capital = 0
        return 4000-100*np.log(capital+1)

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
        if bm.capital < 2000:
            return self.calculateSubsidiaryFormula(bm.capital)
        return 0


    def regulateSubsidiary(self,businessman,govMon, bmList):
        subs = self.robinHoodMode(businessman)
        businessman.subsidiariesHistory.append(subs)
        businessman.capital += subs
        self.governmentMoney -= subs
        # if not self.isPersonHelped(businessman):
        #     # if (businessman.capital < (self.avgCapital * 0.5)):
        #     if businessman.capital < 10000 and self.governmentMoney - self.subsidyValue > 0:
        #         businessman.subsidiaries += self.subsidyValue
        #         self.governmentMoney -= self.subsidyValue
        #         temp = [businessman.id, 0] # We put a pair instead of ID only because later on we will increment the counter to 3 days per subsidiary
        #         self.subsidiariesStatus.append(temp)
        # else:
        #     for subs in self.subsidiariesStatus:
        #         if subs[0] == businessman.id:
        #             self.subsidiariesStatus.remove(subs)
        #             businessman.subsidiaries = 0

    def regulateTax(self, company):
        if company.bruttoProfitHistory[-1] > 0:
            company.taxHistory.append(company.bruttoProfitHistory[-1] * self.taxRate)
            self.governmentMoney += company.taxHistory[-1]

    def regulate(self, businessmenList):
        momentaryGovMoney = self.governmentMoney
        for bm in businessmenList:
            self.regulateSubsidiary(bm, momentaryGovMoney, len(businessmenList))


class PoliticsSwitcher(Enum):

    """Defines the economical strategy of the government"""
    SUPPORTIVE = 1
    NEUTRAL = 0
    COMPETITIVE = -1