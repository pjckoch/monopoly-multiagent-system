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
        #self._price = price
        self.fixedCost = 0.5 * self.price
        self.variableCost = 0.01 * self.frequency * self.price
        self.taxes = 0
        self.profitHistory = []
        self.companyValue = 0

    def computeProfit(self):
        profit = self.turnOver - self.taxes - self.variableCost - self.fixedCost
        # print("PROFIT " + str(self.id))
        # print("price: " + str(self.price))
        # print("turnOver: " + str(self.turnOver))
        # print("taxes: " + str(self.taxes))
        # print("variableCost: " + str(self.variableCost))
        # print("fixedCost: " + str(self.fixedCost))
        # print("RESULT: " + str(profit))
        # print("-----------------------")
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
            self._frequency = np.random.uniform(1,3)                  #np.random number between 1 and 3
        elif self.category == BusinessCategory.SUPERMARKET:
            self._frequency = np.random.uniform(9,10)
        elif self.category == BusinessCategory.RESTAURANT:
            self._frequency = np.random.uniform(4,8)
        elif self.category == BusinessCategory.ENTERTAINMENT:
            self._frequency = np.random.uniform(2,6)
        elif self.category == BusinessCategory.LUXURY:
            self._frequency = np.random.uniform(1,1.5)
        else:
            raise ValueError("Category invalid.")
        return self._frequency
    
    @cached_property
    def necessity(self):
        if self.category == BusinessCategory.MEDICAL:
            self._necessity = np.random.uniform(9,10)
        elif self.category == BusinessCategory.SUPERMARKET:
            self._necessity = np.random.uniform(7,9)
        elif self.category == BusinessCategory.RESTAURANT:
            self._necessity = np.random.uniform(3,5)
        elif self.category == BusinessCategory.ENTERTAINMENT:
            self._necessity = np.random.uniform(1,3)
        elif self.category == BusinessCategory.LUXURY:
            self._necessity = 1.0
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
        return self._price


class BusinessCategory(str, Enum):

    MEDICAL = 'MEDICAL'
    SUPERMARKET = 'SUPERMARKET'
    RESTAURANT = 'RESTAURANT'
    ENTERTAINMENT = 'ENTERTAINMENT'
    LUXURY = 'LUXURY'