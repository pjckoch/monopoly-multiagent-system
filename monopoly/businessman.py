import numpy as np
import random
import pandas as pd
from company import Company

name_list = "lists/names.csv"

df = pd.read_csv(name_list)
full_names = df['full_name']
numLines = len(full_names)

class Businessman():
    """An intelligent agent that interacts with other agents with the objective to maximize his capital."""

    def __init__(self, businessmanId):
        self.id = businessmanId
        self.name = full_names[random.randint(1, numLines)]
        self.capital = 1000 * np.random.randn() + 10000		# sig * randn + mu
        self.happiness = 10 * np.random.randn() + 50		# sig * randn + mu
        self.isAlive = True
        self.subsidiaries = 0
        self.companies = []
        self.dailyActions = []

    def chooseAction(self, company):
        aux = self.considerAction(company)
        if self.considerAction(company) > 0.3:
            self.capital -= company.price
            company.turnOver += company.price #temporary way, change to transaction function
            return company
        else:
            return None

    def considerAction(self, company):
        return self.capital / company.price * 900

    def negotiate(self):
        print("")

    def suicide(self):
        print("")

    def declareBancrupcy(self):
        print("")

    def offerForCompany(self, company, price):
        print(self.happiness)
        if price >= company.companyValue:
            if self.happiness < 60:
                return price
        return 0

    def considerInvestment(self, avgCapital, possibleInvestments):
        if avgCapital - self.capital > 0:
            for cmp in possibleInvestments:
                if self.capital/1.5 > cmp.computeCompanyValue():
                    if random.randint(1,101) > 80 and (avgCapital - self.capital) / avgCapital > 0.1:
                        return cmp
            print("")


    # TODO: Add investments in own companies, Create a new company, Buy a new company
    def invest(self, env):
        categories = []
        for cmp in self.companies:
            categories.append(cmp.category)

        possibleInvestments = env.findCompaniesByCategory(categories)

        company = self.considerInvestment(env.avgCapital, possibleInvestments)

        if company != None:
            owner = env.findCompanyOwner(company)
            price = owner.offerForCompany(company, company.companyValue)
            if price > 0:
                env.sellCompany(company, self, owner, price)
        print("")

    def createCompany(self, companyId):
        """Creates a new company belonging to the businessman who founds it."""
        company = Company(companyId)
        self.companies.append(company)
        return company

    def displayDailyActions(self):
        print("Businessman " + str(self.id) + " Daily Actions:")
        for action in self.dailyActions:
            if action is not None:
                print(action.id)
            else:
                print("No Action")
