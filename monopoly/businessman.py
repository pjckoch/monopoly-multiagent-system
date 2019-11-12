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

    def __init__(self,
                businessmanId,
                name=None,
                capital=1000 * np.random.randn() + 10000,
                happiness=10 * np.random.randn() + 50,
                isAlive=True,
                subsidiaries=0,
                companiesList=None,
                subsidiariesHistory=None):
        self.id = businessmanId
        self.isAlive = isAlive
        self.subsidiaries = subsidiaries
        self.name = full_names[np.random.randint(1, numLines)]
        self.capital = capital
        self.happiness = happiness
        self.companies = [] if companiesList is None else companiesList
        self.subsidiariesHistory = [0] if subsidiariesHistory is None else subsidiariesHistory
    
    def getCompanyOwner(self, company, env):
        for bm in env.listOfPeople:
            for cmp in bm.companies:
                if cmp.id == company.id:
                    return bm
        return None

    def chooseAction(self, env):
        # if the businessman has no cash, he won't do shit
        if self.capital <= 0:
            return None
        # choose a category randomly based on the frequency (probability)
        category = self.chooseCategory()
        # choose a company from that category
        company = self.chooseCompany(category, env.listOfCompanies)
        if company and self.considerAction(company) > 0.3:
            self.capital -= company.price
            # self.getCompanyOwner(company, env).capital += company.price
            company.turnOver += company.price #temporary way, change to transaction function
            return company
        else:
            return None


    def chooseCategory(self):
            allCategories = list(BusinessCategory)
            # pick from the categories list according to the frequency as weights (probability)
            return random.choices(population = allCategories, weights = [cat.value[0] for cat in allCategories])[0]

    def chooseCompany(self, category, companies):
        companiesFromCategory = [c for c in companies if c.category == category]
        # catch the case that there is no company in that category
        if not companiesFromCategory:
            return None
        # check if the businessman owns a company of that type himself, increasing the probability that he goes there
        bmsCompaniesOfThisCategory = [i for i in range(len(self.companies)) if self.companies[i].category == category]
        # if he has a company of that type, he chooses it with 90 % probability
        if bmsCompaniesOfThisCategory and decision(0.9):
            # pick randomly from all his companies that belong to this particular category
            companyIdx = random.choice(bmsCompaniesOfThisCategory)
            company = self.companies[companyIdx]
        # otherwise evaluate the quality of the other companies
        else:
            company = self.pickBasedOnPricePerformance(companiesFromCategory)
        return company

    def pickBasedOnPricePerformance(self, companiesFromCategory):
        # pick randomly from the companies list according to three parameters as weights: PRICE, QUALITY, CAPITAL
        # this is a trade-off in which the businessman likely picks the best value option according to his financial situation
        prices = np.array([comp.price for comp in companiesFromCategory])
        qualities = np.array([comp.quality for comp in companiesFromCategory])
        weights = qualities * np.log(self.capital/1000 +1) + 100/prices
        return random.choices(population = companiesFromCategory, weights = weights)[0]
    
    def considerAction(self, company):
        return self.capital * company.necessity**2 / company.price

    def negotiate(self):
        print("")

    def suicide(self):
        print("")

    def declareBancrupcy(self):
        print("")

    def offerForCompany(self, company, price, avgCapital):
        value = company.companyValue
        willingness = 1/(avgCapital-self.capital)/avgCapital + 1
        chance = willingness - (value-price)/value
        if 1-random.randint(1, 101)/100 > chance:
            return price
        elif price < value:
            return value*(2-(value-price)/value)
        else:
            return price*random.randint(100, 150)/100

    def considerInvestment(self, avgCapital, possibleInvestments):
        if self.capital > 1.2*avgCapital:
            bestValue = 99999999
            bestCompany = None
            for cmp in possibleInvestments:
                v = cmp.companyValue
                if bestValue > v and v > 20:
                    bestCompany = cmp
                    bestValue = v
            if random.randint(1,101) < 30 and bestValue < self.capital*0.2:
                return bestCompany



    # TODO: Add investments in own companies, Create a new company, Buy a new company
    def invest(self, env):

        categories = []
        for cmp in self.companies:
            categories.append(cmp.category)

        possibleInvestments = env.findCompaniesByCategory(categories)

        company = self.considerInvestment(env.avgCapital, possibleInvestments)

        if company != None:
            owner = env.findCompanyOwner(company)
            if owner != self and company.dontSell < 0:
                offer = company.companyValue*random.randint(75, 105)/100
                counter = owner.offerForCompany(company, offer, env.avgCapital)
                if counter == offer:
                    env.sellCompany(company, self, owner, offer)
                else:
                    secondOffer = (((counter-offer)/offer)+1)*random.randint(95, 120)/100
                    secondCounter = owner.offerForCompany(company, secondOffer, env.avgCapital)
                    if secondCounter == secondOffer:
                        env.sellCompany(company, self, owner, secondOffer)
                    else:
                        thirdOffer = (((counter-offer)/offer)+1)*random.randint(95, 120)/100
                        thirdCounter = owner.offerForCompany(company, thirdOffer, env.avgCapital)
                        if thirdCounter == thirdOffer:
                            env.sellCompany(company, self, owner, thirdOffer)

    def createCompany(self, companyId):
        """Creates a new company belonging to the businessman who founds it."""
        company = Company(companyId)
        self.companies.append(company)
        return company

def decision(probability):
    # def investOwnCompany(self, price):
    #     cmpList = self.companies

    #     worstCmpValue = 9999
    #     worstCmp = None
    #     for cmp in cmpList:
    #         if cmp.companyValue < worstCmpValue:
    #             worstCmpValue = cmp.companyValue
    #             worstCmp = cmp
    #     if worstCmp != None:
    #         worstCmp.frequency = worstCmp.frequency  - 1
    #         worstCmp.necessity = worstCmp.necessity - 1
    #         worstCmp.investmentLevel = worstCmp.investmentLevel + 1
    #         self.capital -= price
    #         print("BM " + str(self.id) + " made an investment in company " + str(worstCmp.id))


    # # Calculates the best investment (Buy a Company from another BM, Create a New One or Invest in one of his own companies)
    # def evaluateInvestments(self, env):
    #     option = "none"
    #     buyCompPrice = 1000000
    #     owner = None

    #     # Calculate Buy Company Price
    #     categories = []
    #     for cmp in self.companies:
    #         categories.append(cmp.category)

    #     possibleInvestments = env.findCompaniesByCategory(categories)

    #     company = self.considerInvestment(env.avgCapital, possibleInvestments)

    #     if company != None:
    #         owner = env.findCompanyOwner(company)
    #         buyCompPrice = owner.offerForCompany(company, company.companyValue)
    #         if buyCompPrice < 0:
    #             buyCompPrice = 1000000

    #     # Calculate Investment Price (Regulated By The Government)
    #     investPrice = env.government.investOwnCompPrice

    #     # Calculate Create Company Price (Regulated By The Government)
    #     createCompPrice = env.government.startCompPrice

    #     # Return best option
    #     if (buyCompPrice < investPrice and  buyCompPrice < createCompPrice and env.government.politics == "competitive"):
    #         option = "Buy Company"
    #         price = buyCompPrice
    #     elif (investPrice < buyCompPrice and  investPrice < createCompPrice and env.government.politics == "neutral?"):
    #         option = "Invest"
    #         price = investPrice
    #     else:
    #         option = "Create Company"
    #         price = createCompPrice

    #     ret = []
    #     ret.append(option)
    #     ret.append(price)
    #     ret.append(owner)
    #     ret.append(company)
    #     return ret
    return np.random.random() < probability