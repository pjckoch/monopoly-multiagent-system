import random
from company import Company
from company import BusinessCategory
from government import Government
from businessman import Businessman
import pandas as pd
import helper_funs

# To be parametrized'
# Wealth Distribution - Value from 0.1 to 1 (0.1 concentrated wealth; 1 distributed wealth)
wealthDist = 0.5


class Environment():
    """Defines the environment of the multiagent system."""

    def __init__(self,
                 numPeople=6,
                 numCompanies=None,
                 government=None,
                 listPeople=None,
                 listCompanies=None,
                 numActions=3,
                 suicideCount=0,
                 time=0):
        self.numPeople = numPeople
        self.numCompanies = (4 * self.numPeople) if numCompanies is None else numCompanies
        self.government = Government() if government is None else government
        self.listOfPeople = [Businessman(i) for i in range(self.numPeople)] if listPeople is None else listPeople
        self.listOfCompanies = listCompanies
        self.numActions = numActions
        self.suicideCount = suicideCount
        self.time = time
        self.activeCompanies = []
        
        if self.listOfCompanies is None:
            self.distributeCompanies()
            self.updateActiveCompanies()
        
        # compute initial values for happiness and capital
        self.computeAvgHappiness()
        self.computeAvgCapital()


    def updateActiveCompanies(self):
        actives = []
        for bm in [bm for bm in self.listOfPeople if bm.isAlive]:
            actives.extend(bm.companies)
        self.activeCompanies = actives

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
        self.listOfCompanies = []
        numCompaniesPerBm = self.numCompanies // len(self.listOfPeople)
        remainingCompanies = self.numCompanies % len(self.listOfPeople)
        for _ in range(numCompaniesPerBm):
            for bm in self.listOfPeople:
                self.listOfCompanies.append(bm.createCompany(self.time, len(self.listOfCompanies))) # id increments with every new company
        for _ in range(remainingCompanies):
            bm = random.choice(self.listOfPeople)
            self.listOfCompanies.append(bm.createCompany(self.time, len(self.listOfCompanies)))
            
    def findCompaniesByCategory(self, categories):
        companies = []
        ownedCompanies = []

        for bm in self.listOfPeople:
            for company in bm.companies:
                ownedCompanies.append(company)

        for cmp in ownedCompanies:
            if cmp.category in categories:
                companies.append(cmp)

        return companies

    def findCompanyOwner(self, company):
        for bm in self.listOfPeople:
            for cmp in bm.companies:
                if cmp.id == company.id:
                    return bm
        return None

    def sellCompany(self, company, buyer, seller, price):
        seller.companies.remove(company)
        buyer.companies.append(company)
        helper_funs.transaction(buyer, seller, price)
        company.dontSell = 100

        # print("Transaction: " + seller.name + "'s company " + company.name + " sold to " + buyer.name + " for " + str(price))
