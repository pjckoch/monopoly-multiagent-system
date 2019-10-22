import numpy as np
import random
from environment import Environment
from plot_history import *
import json
from enum import Enum

days = 10

class JsonEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, Enum):
                return obj.name  # Could also be obj.value
            return obj.__dict__

if __name__ == "__main__":

    env = Environment()

    with open("config.json", 'w') as f:
        json.dump(env, f, cls = JsonEncoder, indent=4)
        f.close()

    # print businessmen id's
    print("Businessman IDs:")
    print([bm.id for bm in env.listOfPeople])

    # print companies categories
    print("Company Categories:")
    print([company.category for company in env.listOfCompanies])

    # print average capital and average happiness
    print("Average Capital:")
    print(env.avgCapital)
    print("Average Happiness:")
    print(env.avgHappiness)

    # change this later, one action per loop only
    for time in np.linspace(0.0, days, num = env.numActions * days + 1):

        # we don't need to round here, we only want to exclude the very first value
        if time != 0.0:

            stillALiveBms = [bm for bm in env.listOfPeople if bm.isAlive]
            for bm in stillALiveBms:
                # choose randomly
                companiesForEvaluation = env.listOfCompanies
                action = bm.chooseAction(companiesForEvaluation)
                if action in bm.companies:
                    print("Action of BM " + str(bm.id) + ": " + str(action.category.name) + ", own company <<" + str(action.name) + ">>")
                elif action:
                    print("Action of BM " + str(bm.id) + ": " + str(action.category.name) + ", <<" + str(action.name) + ">>")
                else:
                    print("Action of BM " + str(bm.id) + ": NONE")
                bm.dailyActions.append(action)

                # assuming buying a new company counts as an investment
                bm.invest(env)


                # print("Businessman " + str(bm.id) + " Action:")

            env.time = round(time, 1)
            print("-----------||-----------")
            print("Days passed: " + str(env.time))

            if env.time % 1.0 == 0.0 :

                # Or display the daily auctions
                # for bm in stillALiveBms:
                #     bm.displayDailyActions()
                #     bm.dailyActions = []

                # compute the profits for each businessman
                for bm in stillALiveBms:

                    dailyProfits = []

                    for company in bm.companies:
                        # print("price:" + str(company.price))
                        cmpProfit = company.computeProfit()
                        dailyProfits.append(cmpProfit)
                        company.computeCompanyValue()


                    # append the new values into the peopleProfitDict
                    env.addProfitsForBM(bm.id, dailyProfits)

                    # compute the updated capital for the businessman and print
                    bm.capital += sum(dailyProfits) + bm.subsidiaries
                    env.addCapitalForBM(bm.id, bm.capital)

                # print(env.listOfCompanies)

                for cmp in env.listOfCompanies:
                    cmpProfit = cmp.computeProfit()
                    env.addProfitsForCompany(cmp.id, cmpProfit)

                env.computeAvgCapital()
                env.computeAvgHappiness()
                averageCompany = env.computeAverageCompanyValue()
                env.government.regulate(env.avgCapital, averageCompany, stillALiveBms)
                print("Government Money: " + str(env.government.governmentMoney))
                for bm in env.listOfPeople:
                    print(bm.capital)

    # plot profit history and capital
    plot_all(env.peopleCapitalDict, env.peopleProfitDict, env.companiesProfitDict, env.companiesTypeIds, numDays = days)
