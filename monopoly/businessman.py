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

    def chooseAction(self, company):
        aux = self.considerAction(company)
        if self.considerAction(company) > 0.5:
            self.capital -= company.price
            company.turnOver += company.price #temporary way, change to transaction function
            return company
        else:
            return None

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
