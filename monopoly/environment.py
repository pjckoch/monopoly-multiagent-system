import random
from company import Company
from businessman import Businessman


class Environment():
    """Defines the environment of the multiagent system."""

    def __init__(self):
        self.numPeople = 10
        self.numCompanies = 1 * self.numPeople
        self.listOfPeople = [Businessman(i) for i in range(self.numPeople)]
        self.listOfCompanies = self.distributeCompanies()
        self.numActions = 5     # per day
        self.suicideCount = 0
        self.avgHappiness = 0
        self.avgCapital = 0
        self.peopleProfitDict = {}
        self.time = 0

        # initialize peopleProfitMatrix --> each bm has empty list of profits
        for bm in self.listOfPeople:
            self.peopleProfitDict[bm.id] = []

        # compute initial values for happiness and capital
        self.computeAvgHappiness()
        self.computeAvgCapital()


    def computeAvgHappiness(self):
        """Function to compute the average happiness of all businessmen."""
        self.avgHappiness = 0

        for bm in self.listOfPeople:
            self.avgHappiness += bm.happiness

        self.avgHappiness /= len(self.listOfPeople)


    def computeAvgCapital(self):
        """Function to compute the average capital of all businessmen."""
        self.avgCapital = 0

        for bm in self.listOfPeople:
            self.avgCapital += bm.capital

        self.avgCapital /= len(self.listOfPeople)


    def addProfitsForBM(self, bmId, profit):
        """Function to append a profit for a certain businessman to the peopleProfitDict"""
        self.peopleProfitDict[bmId].append(profit)


    def distributeCompanies(self):
        """Makes every businessman found his first company for himself."""
        for bm in self.listOfPeople:
            bm.foundCompany(bm.id)  # id of first company is sames as BM Id

        return [company for company in bm.companies for bm in self.listOfPeople]
