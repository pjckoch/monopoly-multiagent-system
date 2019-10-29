import random
from company import Company
from company import BusinessCategory
from government import Government
from businessman import Businessman
import pandas as pd

# To be parametrized'
# Wealth Distribution - Value from 0.1 to 1 (0.1 concentrated wealth; 1 distributed wealth)
wealthDist = 0.5


class Environment():
    """Defines the environment of the multiagent system."""

    def __init__(self):
        self.numPeople = 10
        self.numCompanies = 4 * self.numPeople
        self.government = Government()
        self.listOfPeople = [Businessman(i) for i in range(self.numPeople)]
        self.listOfCompanies = []
        self.numActions = 2     # per day
        self.suicideCount = 0
        self.avgHappiness = 0
        self.avgCapital = 0
        self.dataframe = pd.DataFrame()
        self.time = 0

        self.distributeCompanies()

        # initialize peopleProfitMatrix --> each bm has empty list of profits
        # for bm in self.listOfPeople:
        #     self.peopleProfitDict[bm.id] = []
        #     self.peopleCapitalDict[bm.id] = []

        # for cmp in self.listOfCompanies:
        #     self.companiesProfitDict[cmp.id] = []

        # for item in list(BusinessCategory):
        #     self.companiesTypeIds[item.name] = []

        # for cmp in self.listOfCompanies:
        #     self.companiesTypeIds[cmp.category.name].append(cmp.id)

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


    # def addProfitsForBM(self, bmId, profit):
    #     """Function to append a profit for a certain businessman to the peopleProfitDict"""
    #     self.peopleProfitDict[bmId].append(profit)


    # def addCapitalForBM(self, bmId, capital):
    #     """Function to append a profit for a certain businessman to the peopleProfitDict"""
    #     self.peopleCapitalDict[bmId].append(capital)
        

    # def addProfitsForCompany(self, cmpId, profit):
    #     """Function to append a profit for a certain businessman to the peopleProfitDict"""
    #     self.companiesProfitDict[cmpId].append(profit)


    def distributeCompanies(self):
        """Makes every businessman create his first company for himself."""
        numCompaniesPerBm = self.numCompanies // len(self.listOfPeople)
        remainingCompanies = self.numCompanies % len(self.listOfPeople)
        for _ in range(numCompaniesPerBm):
            for bm in self.listOfPeople:
                self.listOfCompanies.append(bm.createCompany(len(self.listOfCompanies))) # id increments with every new company
        for _ in range(remainingCompanies):
            bm = random.choice(self.listOfPeople)
            self.listOfCompanies.append(bm.createCompany(len(self.listOfCompanies)))
            
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
