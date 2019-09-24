import numpy as np
import random
from environment import Environment
from plot_history import *

days = 100

if __name__ == "__main__":

    environment = Environment()

    # print businessmen id's
    print("Businessman IDs:")
    print([bm.id for bm in environment.listOfPeople])

    # print companies id's
    print("Company IDs:")
    print([company.id for company in environment.listOfCompanies])

    # print average capital and average happiness
    print("Average Capital:")
    print(environment.avgCapital)
    print("Average Happiness:")
    print(environment.avgHappiness)

    # change this later, one action per loop only
    for time in np.linspace(0.0, days, num = environment.numActions * days + 1):

        # we don't need to round here, we only want to exclude the very first value
        if time != 0.0:

            stillALiveBms = [bm for bm in environment.listOfPeople if bm.isAlive]
            for bm in stillALiveBms:
                
                # choose randomly
                companiesForEvaluation = []

                for i in range(environment.numActions):
                    companiesForEvaluation.append(environment.listOfCompanies[random.randint(0, len(environment.listOfCompanies)-1)])

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
            environment.time = round(time, 1)
            print("Days passed: " + str(environment.time))

            if environment.time % 1.0 == 0.0 :

                # compute the profits for each businessman
                for bm in stillALiveBms:

                    dailyProfits = []

                    for company in bm.companies:

                        dailyProfits.append(company.computeProfit())
                        #dailyProfits.append(np.random.randint(low = -1000, high = 1000))

                    # append the new values into the peopleProfitDict
                    environment.addProfitsForBM(bm.id, dailyProfits)

                    # compute the updated capital for the businessman and print
                    bm.capital += sum(dailyProfits)
                    printmsg = "Businessman " + str(bm.id)
                    printmsg += " capital after " + str(time) + " days: "
                    printmsg += str(bm.capital)
                    print(printmsg)

                    # """if bm.id == 0 or bm.id == 1:
                    #     plotCapitalHistory(bm.capital, bm.id, int(environment.time))
                    # """

    # print the profit history for each businessman
    print("People Profit Dictionary after " + str(days) + " days:")
    print(environment.peopleProfitDict)
    print("COMPANY ID: ",environment.listOfCompanies[0].id)
    print("COMPANY frequency: ",environment.listOfCompanies[0].frequency)
    print("COMPANY necessity: " ,environment.listOfCompanies[0].necessity)
    print("COMPANY price: " ,environment.listOfCompanies[0].price)
    print("COMPANY variableCost: " ,environment.listOfCompanies[0].variableCost)
    print("COMPANY fixedCost: " ,environment.listOfCompanies[0].fixedCost)

    # plot the profitHistory
    plotProfitHistory(environment.peopleProfitDict, bmIds = [0, 1, 2], numDays = days)
