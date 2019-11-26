import numpy as np
import random
import pandas as pd
from enum import Enum
from django.utils.functional import cached_property

company_list = "lists/companies.csv"

df = pd.read_csv(company_list)
company_names = df['fake-company-name']
numLines = len(company_names)

class Company():
    """Company Object."""

    # TODO

    # The higher de turnOver, the higher the taxes
    # The price is calculated according to the frequency and the necessity
    # The fixed costs are higher based on how high the necessity is
    # The variable costs are higher based on how high the frequency is
    # Initial Taxes for every Company, then the government adjusts

    def __init__(self,
                 companyId,
                 name=None,
                 category=None,
                 frequency=None,
                 necessity=None,
                 price=None,
                 quality=None,
                 turnOver=0,
                 fixedCost=None,
                 variableCost=None,
                 companyValue=0,
                 investmentLevel=0,
                 bruttoProfitHistory=None,
                 nettoProfitHistory=None,
                 turnOverHistory=None,
                 dontSell=None,
                 taxHistory=None,
                 demandHistory=None,
                 costHistory=None):
        self.id = companyId
        self.inflationFactor = 1
        self.name = company_names[np.random.randint(1, numLines)] if name is None else name
        self.category = random.choice(list(BusinessCategory)) if category is None else category
        self.frequency = self.category.value[0] if frequency is None else frequency
        self.necessity = self.category.value[1] if necessity is None else necessity
        if price is None:
            self.price
        else:
            self.price = price
        if quality is None:
            self.quality
        else:
            self.quality = quality
        self.fixedCost = (self.price) if fixedCost is None else fixedCost
        self.variableCost = (0.1 * self.price) if variableCost is None else variableCost
        self.turnOver = turnOver
        self.companyValue = companyValue
        self.investmentLevel = investmentLevel
        self.bruttoProfitHistory = [] if bruttoProfitHistory is None else bruttoProfitHistory
        self.nettoProfitHistory = [] if nettoProfitHistory is None else nettoProfitHistory
        self.turnOverHistory = [] if turnOverHistory is None else turnOverHistory
        self.taxHistory = [0] if taxHistory is None else taxHistory
        self.dontSell = 10
        self.companySales = []
        self.demand = 0
        self.demandHistory = [] if demandHistory is None else demandHistory
        self.costHistory = [] if costHistory is None else costHistory
        
    def isBankrupting(self):
        if (len(self.nettoProfitHistory) > 10):
            if sum(self.nettoProfitHistory[-9:]) < 0:
                return True

        return False

    def bankrupcy(self, env):
        if self.isBankrupting():
            owner = env.findCompanyOwner(self)
            env.government.governmentMoney -= self.fixedCost*30
            owner.capital += self.fixedCost*30
            owner.loseCompany(self)

    def computeBruttoProfit(self):
        """Compute profit without considering taxes"""
        self.turnOverHistory.append(self.turnOver)
        totalCosts = self.variableCost * self.demand + self.fixedCost
        self.costHistory.append(totalCosts)
        bProfit = self.turnOver - totalCosts
        self.bruttoProfitHistory.append(bProfit)
        self.demandHistory.append(self.demand)
        self.demand = 0
        self.turnOver = 0
        return bProfit

    def computeNettoProfit(self):
        """Profit minus taxes"""
        bProfit = self.bruttoProfitHistory[-1]
        tax = self.taxHistory[-1]
        nProfit = bProfit - tax
        self.nettoProfitHistory.append(nProfit)
        return nProfit

    def computeCompanyValue(self):
        if (len(self.nettoProfitHistory) > 4):
            self.companyValue = 10*sum(self.nettoProfitHistory[-5:])
        return self.companyValue

    def payCosts(self, government):
        """Paying the costs (going to the government ATM)"""
        government.governmentMoney += self.costHistory[-1]

    def updateSale(self):
        self.dontSell = self.dontSell - 1

    def visited(self):
        self.demand += 1 

    @property
    def frequency(self):
        return self._frequency
    @frequency.setter
    def frequency(self, value):
        self._frequency = value

    @property
    def necessity(self):
        return self._necessity
    @necessity.setter
    def necessity(self, value):
        self._necessity = value

    @cached_property
    def price(self):
        if self.category == BusinessCategory.MEDICAL:
            self._price = (0.5 * np.random.randn() + 10*5) * self.inflationFactor 	        # sig * randn + mu
        elif self.category == BusinessCategory.SUPERMARKET:
            self._price = (0.1 * np.random.randn() + 1*5) * self.inflationFactor  	
        elif self.category == BusinessCategory.RESTAURANT:
            self._price = (0.25 * np.random.randn() + 17.5/5*5)	* self.inflationFactor 
        elif self.category == BusinessCategory.ENTERTAINMENT:
            self._price = (0.25 * np.random.randn() + 4*5) * self.inflationFactor 	
        elif self.category == BusinessCategory.LUXURY:
            self._price = (2 * np.random.randn() + 30*5) * self.inflationFactor 
        else:
            raise ValueError("Category invalid.")
        return self._price * (1 + self.quality) * self.inflationFactor 

    @cached_property
    def quality(self):
        self._quality = np.random.uniform(0.0, 1.0)                 # 0.0: low, 1.0: high quality
        return self._quality


class BusinessCategory(Enum):

    """ Name = (Frequency, Necessity)"""
    MEDICAL = (0.1, 0.9)
    SUPERMARKET = (0.45, 0.8)
    RESTAURANT = (0.2, 0.4)
    ENTERTAINMENT = (0.2, 0.3)
    LUXURY = (0.05, 0.1)