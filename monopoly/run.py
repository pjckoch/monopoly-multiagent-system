import numpy as np
import random
from environment import Environment
from plot_history import *
import params
import json

days = 2

class MyEncoder(json.JSONEncoder):
        def default(self, o):
            return o.__dict__  

if __name__ == "__main__":

    env = Environment()

    with open("config.json", 'w') as f:
        json.dump(env, f, cls = MyEncoder, indent=4)

    # print businessmen id's
    print("Businessman IDs:")
    print([bm.id for bm in env.listOfPeople])

    # print companies id's
    print("Company IDs:")
    print([company.id for company in env.listOfCompanies])

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
                companiesForEvaluation = []

                for i in range(env.numActions):
                    companiesForEvaluation.append(env.listOfCompanies[random.randint(0, len(env.listOfCompanies)-1)])

                bmDailyActions = []
                for company in companiesForEvaluation:
                    aux = bm.chooseAction(company)
                    bmDailyActions.append(aux)

                print("Businessman " + str(bm.id) + " List of Actions:")
                for action in bmDailyActions:
                    if action is not None:
                        print(action.id)
                    else:
                        print("No action")
            env.time = round(time, 1)
            print("Days passed: " + str(env.time))

            if env.time % 1.0 == 0.0 :

                # compute the profits for each businessman
                for bm in stillALiveBms:

                    dailyProfits = []

                    for company in bm.companies:

                        dailyProfits.append(company.computeProfit())
                        

                    # append the new values into the peopleProfitDict
                    env.addProfitsForBM(bm.id, dailyProfits)

                    # compute the updated capital for the businessman and print
                    bm.capital += sum(dailyProfits)
                    env.addCapitalForBM(bm.id, bm.capital)


    # print some values
    print("COMPANY ID: ",env.listOfCompanies[0].id)
    print("COMPANY frequency: ",env.listOfCompanies[0].frequency)
    print("COMPANY necessity: " ,env.listOfCompanies[0].necessity)
    print("COMPANY price: " ,env.listOfCompanies[0].price)
    print("COMPANY variableCost: " ,env.listOfCompanies[0].variableCost)
    print("COMPANY fixedCost: " ,env.listOfCompanies[0].fixedCost)

    # plot profit history and capital
    plot_all(env.peopleCapitalDict, env.peopleProfitDict, numDays = days)
