import random
from company import Company
from government import Government
from businessman import Businessman
# from government import Government

# To be parametrized'
# Wealth Distribution - Value from 0.1 to 1 (0.1 concentrated wealth; 1 distributed wealth)
wealthDist = 0.5


class Environment():
    """Defines the environment of the multiagent system."""

    def __init__(self):
        self.numPeople = 3
        # self.gov = Government()
        self.numCompanies = 2 * self.numPeople
        self.government = Government()
        self.listOfPeople = [Businessman(i) for i in range(self.numPeople)]
        self.listOfCompanies = self.distributeCompanies()
        self.numActions = 2     # per day
        self.suicideCount = 0
        self.avgHappiness = 0
        self.avgCapital = 0
        self.peopleProfitDict = {}
        self.peopleCapitalDict = {}
        self.time = 0

        # initialize peopleProfitMatrix --> each bm has empty list of profits
        for bm in self.listOfPeople:
            self.peopleProfitDict[bm.id] = []
            self.peopleCapitalDict[bm.id] = []


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

    def computeAverageCompanyValue(self):
        """Function to compute the average company value"""
        temp = 0
        for company in self.listOfCompanies:
            temp += company.companyValue
        return temp/len(self.listOfCompanies)


    def addProfitsForBM(self, bmId, profit):
        """Function to append a profit for a certain businessman to the peopleProfitDict"""
        self.peopleProfitDict[bmId].append(profit)


    def addCapitalForBM(self, bmId, capital):
        """Function to append a profit for a certain businessman to the peopleProfitDict"""
        self.peopleCapitalDict[bmId].append(capital)


    def distributeCompanies(self):
        """Makes every businessman found his first company for himself."""
        for bm in self.listOfPeople:
            bm.foundCompany(bm.id)  # id of first company is sames as BM Id

        return [company for bman in self.listOfPeople for company in bman.companies]

    def findCompaniesByCategory(self, categories):
        companies = []
        for cmp in self.listOfCompanies:
            if cmp.category in categories:
                companies.append(cmp)

        return companies

    def findCompanyOwner(self, company):
        for bm in self.listOfPeople:
            for cmp in bm.companies:
                if cmp == company:
                    return bm
        return None

    def sellCompany(self, company, buyer, seller, price):
        seller.companies.remove(company)
        buyer.companies.append(company)
        seller.capital += price
        buyer.capital -= price

        print("Transaction: " + seller.name + "'s company " + company.name + " sold to " + buyer.name + " for " + str(price))
