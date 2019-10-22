import numpy as np
import pandas as pd
from company import Company, BusinessCategory
import random

name_list = "lists/names.csv"

df = pd.read_csv(name_list)
full_names = df['full_name']
numLines = len(full_names)

class Businessman():
    """An intelligent agent that interacts with other agents with the objective to maximize his capital."""

    def __init__(self, businessmanId):
        self.id = businessmanId
        self.name = full_names[np.random.randint(1, numLines)]
        self.capital = 1000 * np.random.randn() + 10000		# sig * randn + mu
        self.happiness = 10 * np.random.randn() + 50		# sig * randn + mu
        self.isAlive = True
        self.subsidiaries = 0
        self.companies = []
        self.dailyActions = []

    def chooseAction(self, companies):
        category = random.choice(list(BusinessCategory))
        company = self.chooseCompany(category, companies)
        if company and self.considerAction(company) > 0.3:
            self.capital -= company.price
            company.turnOver += company.price #temporary way, change to transaction function
            return company
        else:
            return None

    def considerAction(self, company):
        return self.capital / company.price * 900

    def chooseCompany(self, category, companies):
        companiesFromCategory = [c for c in companies if c.category == category]
        print(category, companiesFromCategory)
        # catch the case that there is no company in that category
        if not companiesFromCategory:
            return None
        company = random.choice(companiesFromCategory)  # to be more intelligent in the future
        return company



    def negotiate(self):
        print("")

    def suicide(self):
        print("")

    def declareBancrupcy(self):
        print("")

    def offerForCompany(self, company, price):
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

    def investOwnCompany(self, price):
        cmpList = self.companies

        worstCmpValue = 9999
        worstCmp = None
        for cmp in cmpList:
            if cmp.companyValue < worstCmpValue:
                worstCmpValue = cmp.companyValue
                worstCmp = cmp
        if worstCmp != None:
            worstCmp.frequency = worstCmp.frequency  - 1
            worstCmp.necessity = worstCmp.necessity - 1
            worstCmp.investmentLevel = worstCmp.investmentLevel + 1
            self.capital -= price
            print("BM " + str(self.id) + " made an investment in company " + str(worstCmp.id))


    # Calculates the best investment (Buy a Company from another BM, Create a New One or Invest in one of his own companies)
    def evaluateInvestments(self, env):
        option = "none"
        buyCompPrice = 1000000
        owner = None

        # Calculate Buy Company Price
        categories = []
        for cmp in self.companies:
            categories.append(cmp.category)

        possibleInvestments = env.findCompaniesByCategory(categories)

        company = self.considerInvestment(env.avgCapital, possibleInvestments)

        if company != None:
            owner = env.findCompanyOwner(company)
            buyCompPrice = owner.offerForCompany(company, company.companyValue)
            if buyCompPrice < 0:
                buyCompPrice = 1000000

        # Calculate Investment Price (Regulated By The Government)
        investPrice = env.government.investOwnCompPrice

        # Calculate Create Company Price (Regulated By The Government)
        createCompPrice = env.government.startCompPrice

        # Return best option
        if (buyCompPrice < investPrice and  buyCompPrice < createCompPrice and env.government.politics == "competitive"):
            option = "Buy Company"
            price = buyCompPrice
        elif (investPrice < buyCompPrice and  investPrice < createCompPrice and env.government.politics == "neutral?"):
            option = "Invest"
            price = investPrice
        else:
            option = "Create Company"
            price = createCompPrice

        ret = []
        ret.append(option)
        ret.append(price)
        ret.append(owner)
        ret.append(company)
        return ret


    # TODO: Add investments in own companies, Create a new company, Buy a new company
    def invest(self, env):
        evaluation = self.evaluateInvestments(env)
        if (self.capital > evaluation[1]):
            # Buy an existing company
            if (evaluation[0]  == "Buy Company"):
                if evaluation[1] > 0:
                    print("EVALUATION OPTION: " + str(evaluation[0]))
                    print("EVALUATION Price: " + str(evaluation[1]))
                    env.sellCompany(evaluation[3], self, evaluation[2], evaluation[1])
            # Investing in own company
            # TODO: Remove Only investing in first company
            elif (evaluation[0]  == "Invest" and self.companies[0].investmentLevel == 0):
                print("EVALUATION OPTION: " + str(evaluation[0]))
                print("EVALUATION Price: " + str(evaluation[1]))
                self.investOwnCompany(evaluation[1])
            # Create a new company
            elif (evaluation[0]  == "Create Company"):
                print()
        # else:
        #     print("No Investment")

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
