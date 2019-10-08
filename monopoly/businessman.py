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

    def invest(self):
        print("")

    def foundCompany(self, companyId):
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
