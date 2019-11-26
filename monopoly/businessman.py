import numpy as np
import pandas as pd
from company import Company, BusinessCategory
import random
import logger
import helper_funs
import math as m

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
        self.name = full_names[np.random.randint(1, numLines)] if name is None else name
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

    def chooseAction(self, companies, env):
        # if the businessman has no cash, he won't do shit
        if self.capital <= 0:
            return None
        # choose a category randomly based on the frequency (probability)

        category = self.chooseCategory()
        # choose a company from that category
        company = self.chooseCompany(category, companies)
        if company and self.considerAction(company):

            ######################################
            # THIS IS THE TEMPORARY BUG FIX
            for bm in env.listOfPeople:
                for comp in bm.companies:
                    if comp.id == company.id:
                        company = comp

            ######################################

            # Append action 
            company.companySales.append(self.id)
            helper_funs.transaction(self, company, company.price)
            company.visited()

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
        bmsCompaniesOfThisCategory = [i for i in range(len(companies)) if companies[i].category == category]
        # if he has a company of that type, he chooses it with 90 % probability
        if bmsCompaniesOfThisCategory and decision(0.9):
            # pick randomly from all his companies that belong to this particular category
            companyIdx = random.choice(bmsCompaniesOfThisCategory)
            company = companies[companyIdx]
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
        sum_weights = sum(weights)
        normal_weights = np.true_divide(weights, sum_weights)
        return random.choices(population = companiesFromCategory, weights = normal_weights)[0]
    
    def considerAction(self, company):
        nec = company.necessity
        p = company.price
        probabilityOfAction = (nec*p*self.capital ) /(p*nec*self.capital + 10000/nec)
        return decision(probabilityOfAction)

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
            if random.randint(1,101) < 30 and bestValue < self.capital*0.8:
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
                #print("First Offer: " + str(offer) + " Value: " + str(company.companyValue))
                counter = owner.offerForCompany(company, offer, env.avgCapital)
                if counter == offer:
                    env.sellCompany(company, self, owner, offer)
                    logger.log_acquireCompany(env.time, self, owner, company, offer)
                else:
                    secondOffer = (((counter-offer)/offer)+1)*random.randint(95, 120)/100*counter
                    secondCounter = owner.offerForCompany(company, secondOffer, env.avgCapital)
                    #print("Second Offer: " + str(secondOffer) + " Value: " + str(company.companyValue))
                    if secondCounter == secondOffer:
                        env.sellCompany(company, self, owner, secondOffer)
                        logger.log_acquireCompany(env.time, self, owner, company, offer)
                    else:
                        thirdOffer = (((counter-offer)/offer)+1)*random.randint(95, 120)/100*secondCounter
                        thirdCounter = owner.offerForCompany(company, thirdOffer, env.avgCapital)
                        if thirdCounter == thirdOffer:
                            env.sellCompany(company, self, owner, thirdOffer)
                            logger.log_acquireCompany(env.time, self, owner, company, offer)
        elif self.capital > 9000:
            if random.randint(1, 10000) > 9999:
                newCompany = self.createCompany(env.time, len(env.listOfCompanies))
                helper_funs.transaction(self, env.government, 5000)
                env.listOfCompanies.append(newCompany)
                print("New company founded by: " + str(self.id))

    def createCompany(self, time, companyId):
        """Creates a new company belonging to the businessman who founds it."""
        company = Company(companyId)
        self.companies.append(company)
        logger.log_createCompany(time, self, company)
        return company

    def loseCompany(self, cmp):
        self.companies.remove(cmp)

def decision(probability):
    return np.random.random() < probability