import numpy as np
import random
from company import Company

class Businessman():
    """An intelligent agent that interacts with other agents with the objective to maximize his capital."""

    def __init__(self, businessmanId):
        self.id = businessmanId
        self.capital = 1000 * np.random.randn() + 10000		# sig * randn + mu
        self.happiness = 10 * np.random.randn() + 50		# sig * randn + mu
        self.isAlive = True
        self.subsidiaries = 500000 * 1 / (self.capital + 1000)
        self.companies = []

    def chooseAction(self, nChoices, allCompanies):
        # choose randomly
        companiesForEvaluation = []
        actions = []

        for i in range(nChoices):
            companiesForEvaluation.append(allCompanies[random.randint(0, len(allCompanies)-1)])

        # for each one, choose to do it or not
        for company in companiesForEvaluation:
            aux = self.considerAction(company)
            if self.considerAction(company) > 0.5:
                actions.append(company)
                self.capital -= company.price
                company.turnOver += company.price #temporary way, change to transaction function

        print("")

        return actions

    def considerAction(self, company):
        return company.price * 900 / self.capital

    def negotiate(self):
        print("")

    def suicide(self):
        print("")

    def declareBancrupcy(self):
        print("")

    def invest(self):
        print("")

    def foundCompany(self, companyId):
        """Creates a new company belonging to the businessman who founds it."""
        company = Company(companyId)
        self.companies.append(company)
        return company
