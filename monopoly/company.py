import numpy as np
import random
import pandas as pd

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
        self.name = company_names[random.randint(0, numLines)]
        self.frequency = random.randint(1,10)   #random number between 1 and 10
        self.necessity = random.randint(1,10)   #random number between 1 and 10
        self.price = 0.8 * self.frequency + 0.8 * self.necessity
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
