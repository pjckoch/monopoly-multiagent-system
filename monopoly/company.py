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

    def __init__(self, companyId):
        self.id = companyId
        self.name = company_names[np.random.randint(0, numLines)]
        self.category = random.choice(list(BusinessCategory))
        # call frequency and necessity to add the to the JSON config
        self.frequency
        self.necessity
        self.turnOver = 0
        self.fixedCost = 0.5 * self.price
        self.variableCost = 0.02 * self.frequency * self.price #0.01 makes it balanced
        self.taxes = 0
        self.profitHistory = []
        self.companyValue = 0
        self.investmentLevel = 0

    def computeProfit(self):
        profit = self.turnOver - self.taxes - self.variableCost - self.fixedCost + 100 * self.investmentLevel
        self.profitHistory.append(profit)
        self.turnOver = 0
        return profit

    # def updateTaxes(self):
    #     print("")

    def computeCompanyValue(self):
        if (len(self.profitHistory) > 4):
            self.companyValue = self.profitHistory[-5] + self.profitHistory[-4] + self.profitHistory[-3] + self.profitHistory[-2] + self.profitHistory[-1]
        # print("COMPANY " + str(self.id) + " VALUE :" )
        # print(self.companyValue)
        return self.companyValue

    @property
    def frequency(self):
        self._frequency = self.category.value[0]
        return self._frequency

    @property
    def necessity(self):
        self._necessity = self.category.value[1]
        return self._necessity

    @cached_property
    def price(self):
        if self.category == BusinessCategory.MEDICAL:
            self._price = 10 * np.random.randn() + 100 		        # sig * randn + mu
        elif self.category == BusinessCategory.SUPERMARKET:
            self._price = 2 * np.random.randn() + 10
        elif self.category == BusinessCategory.RESTAURANT:
            self._price = 5 * np.random.randn() + 35
        elif self.category == BusinessCategory.ENTERTAINMENT:
            self._price = 5 * np.random.randn() + 40
        elif self.category == BusinessCategory.LUXURY:
            self._price = 40 * np.random.randn() + 300
        else:
            raise ValueError("Category invalid.")
        return self._price * (1 + self.quality)

    @cached_property
    def quality(self):
        self._quality = np.random.uniform(0.0, 1.0)                 # 0.0: low, 1.0: high quality
        return self._quality


class BusinessCategory(Enum):

    # Name = (Frequency, Necessity)
    MEDICAL = (0.1, 0.9)
    SUPERMARKET = (0.45, 0.8)
    RESTAURANT = (0.2, 0.4)
    ENTERTAINMENT = (0.2, 0.3)
    LUXURY = (0.05, 0.1)