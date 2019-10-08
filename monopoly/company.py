import numpy as np
import random
import pandas as pd
from enum import Enum

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
        self.fixedCost = 0.5 * self.necessity
        self.variableCost = 0.5 * self.frequency
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

    @property
    def frequency(self):
        if self.category == BusinessCategory.MEDICAL:
            return np.random.randint(1,3)                  #np.random number between 1 and 3
        elif self.category == BusinessCategory.SUPERMARKET:
            return np.random.randint(8,10)
        elif self.category == BusinessCategory.RESTAURANT:
            return np.random.randint(4,8)
        elif self.category == BusinessCategory.ENTERTAINMENT:
            return np.random.randint(2,6)
        elif self.category == BusinessCategory.LUXURY:
            return np.random.randint(1,3)
        else:
            raise ValueError("Category invalid.")
    
    @property
    def necessity(self):
        if self.category == BusinessCategory.MEDICAL:
            return np.random.randint(8,10)
        elif self.category == BusinessCategory.SUPERMARKET:
            return np.random.randint(7,9)
        elif self.category == BusinessCategory.RESTAURANT:
            return np.random.randint(3,5)
        elif self.category == BusinessCategory.ENTERTAINMENT:
            return np.random.randint(1,3)
        elif self.category == BusinessCategory.LUXURY:
            return np.random.randint(1,2)
        else:
            raise ValueError("Category invalid.")

    @property
    def price(self):
        if self.category == BusinessCategory.MEDICAL:
            return 10 * np.random.randn() + 200 		        # sig * randn + mu
        elif self.category == BusinessCategory.SUPERMARKET:
            return 2 * np.random.randn() + 10
        elif self.category == BusinessCategory.RESTAURANT:
            return 5 * np.random.randn() + 25
        elif self.category == BusinessCategory.ENTERTAINMENT:
            return 5 * np.random.randn() + 25
        elif self.category == BusinessCategory.LUXURY:
            return 100 * np.random.randn() + 300
        else:
            raise ValueError("Category invalid.")


class BusinessCategory(str, Enum):

    MEDICAL = 'MEDICAL'
    SUPERMARKET = 'SUPERMARKET'
    RESTAURANT = 'RESTAURANT'
    ENTERTAINMENT = 'ENTERTAINMENT'
    LUXURY = 'LUXURY'