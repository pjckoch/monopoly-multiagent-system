import numpy as np
import random
from environment import Environment
from plot_history import *
from enum import Enum
import data_manager

days = 360
evaluationInterval = data_manager.EvaluationInterval.DAILY

# def runFromJson(jsonFile):

#     env = data_manager.readFromJson(jsonFile)


if __name__ == "__main__":

    configFile = "config.json"
    env = Environment()
    data_manager.writeToJson(configFile, env)
    totalMoney = 0
    # runFromJson(configFile)

    # change this later, one action per loop only
    for time in np.linspace(0.0, days, num = env.numActions * days + 1):
        totalMoney = 0
        # we don't need to round here, we only want to exclude the very first value
        if time != 0.0:

            stillALiveBms = [bm for bm in env.listOfPeople if bm.isAlive]
            companiesForEvaluation = env.listOfCompanies

            for bm in stillALiveBms:

                action = bm.chooseAction(companiesForEvaluation, env)
                bm.dailyActions.append(action)
                # assuming buying a new company counts as an investment
                # bm.invest(env)
                totalMoney += bm.capital

            env.time = round(time, 1)

            if env.time % evaluationInterval.value == 0.0 :

                # compute the profits for each businessman
                for bm in stillALiveBms:

                    for company in bm.companies:
                        nProfit = company.computeNettoProfit()            
                        company.payCosts(env.government)            
                        company.computeCompanyValue()

                    # compute the updated capital for the businessman and print
                    # bm.capital += nProfit + bm.subsidiaries
                    bm.capital += nProfit 

                averageCompany = env.computeAverageCompanyValue()
                # env.government.regulate(env.avgCapital, averageCompany, stillALiveBms)
                env.computeAvgCapital()
                env.computeAvgHappiness()
                data_manager.evaluateStats(time, evaluationInterval, env.listOfPeople)

                # print("Government Money: " + str(env.government.governmentMoney))
                # for bm in env.listOfPeople:
                #     print(round(bm.capital,0))
        totalMoney += env.government.governmentMoney

    # plot profit history and capital
    data_manager.exportToCSV()
    # data_manager.writeToJson("results.json", env)