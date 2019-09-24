import numpy as np
import random
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
        self.frequency = random.randint(1,10)   #random number between 1 and 10
        self.necessity = random.randint(1,10)   #random number between 1 and 10
        self.price = 5 * self.frequency + 5 * self.necessity
        self.turnOver = 0
        self.fixedCost = 5 * self.necessity
        self.variableCost = 5 * self.frequency
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
        print("")
