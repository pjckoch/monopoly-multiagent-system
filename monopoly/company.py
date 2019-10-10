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
        self.turnOver = 0
        self.fixedCost = 0.5 * self.price
        self.variableCost = 0.01 * self.frequency * self.price
        self.taxes = 0
        self.profitHistory = []
        self.companyValue = 0

    def computeProfit(self):
        profit = self.turnOver - self.taxes - self.variableCost - self.fixedCost
        self.profitHistory.append(profit)
        self.turnOver = 0
        return profit

    def updateTaxes(self):
        print("")

    def computeCompanyValue(self):
        if (len(self.profitHistory) > 4):
            self.companyValue = self.profitHistory[-5] + self.profitHistory[-4] + self.profitHistory[-3] + self.profitHistory[-2] + self.profitHistory[-1]
        print("COMPANY VALUE: " + str(self.id))
        print(self.companyValue)
        return self.companyValue

    @cached_property
    def frequency(self):
        if self.category == BusinessCategory.MEDICAL:
            self._frequency = 0.1
        elif self.category == BusinessCategory.SUPERMARKET:
            self._frequency = 0.45
        elif self.category == BusinessCategory.RESTAURANT:
            self._frequency = 0.2
        elif self.category == BusinessCategory.ENTERTAINMENT:
            self._frequency = 0.2
        elif self.category == BusinessCategory.LUXURY:
            self._frequency = 0.05
        else:
            raise ValueError("Category invalid.")
        return self._frequency
    
    @cached_property
    def necessity(self):
        if self.category == BusinessCategory.MEDICAL:
            self._necessity = 0.9
        elif self.category == BusinessCategory.SUPERMARKET:
            self._necessity = 0.8
        elif self.category == BusinessCategory.RESTAURANT:
            self._necessity = 0.4
        elif self.category == BusinessCategory.ENTERTAINMENT:
            self._necessity = 0.3
        elif self.category == BusinessCategory.LUXURY:
            self._necessity = 0.1
        else:
            raise ValueError("Category invalid.")
        return self._necessity

    @cached_property
    def price(self):
        if self.category == BusinessCategory.MEDICAL:
            self._price = 10 * np.random.randn() + 150 		        # sig * randn + mu
        elif self.category == BusinessCategory.SUPERMARKET:
            self._price = 2 * np.random.randn() + 10
        elif self.category == BusinessCategory.RESTAURANT:
            self._price = 5 * np.random.randn() + 30
        elif self.category == BusinessCategory.ENTERTAINMENT:
            self._price = 5 * np.random.randn() + 40
        elif self.category == BusinessCategory.LUXURY:
            self._price = 40 * np.random.randn() + 200
        else:
            raise ValueError("Category invalid.")
        return self._price * (1 + self.quality)

    @cached_property
    def quality(self):
        self._quality = np.random.uniform(0.0, 1.0)                 # 0.0: low, 1.0: high quality
        return self._quality
        

class BusinessCategory(str, Enum):

    MEDICAL = 'MEDICAL'
    SUPERMARKET = 'SUPERMARKET'
    RESTAURANT = 'RESTAURANT'
    ENTERTAINMENT = 'ENTERTAINMENT'
    LUXURY = 'LUXURY'