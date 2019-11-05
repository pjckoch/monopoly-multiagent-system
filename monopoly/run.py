import numpy as np
import pandas as pd
import random
from environment import Environment
from plot_history import *
from enum import Enum
import data_manager

days = 90
evaluationInterval = data_manager.EvaluationInterval.MONTHLY

def runFromJson(jsonFile):

    env = data_manager.readFromJson(jsonFile)

    # change this later, one action per loop only
    for time in np.linspace(0.0, days, num = env.numActions * days + 1):

        # we don't need to round here, we only want to exclude the very first value
        if time != 0.0:

            stillALiveBms = [bm for bm in env.listOfPeople if bm.isAlive]
            companiesForEvaluation = env.listOfCompanies

            for bm in stillALiveBms:

                action = bm.chooseAction(companiesForEvaluation)
                # assuming buying a new company counts as an investment
                bm.invest(env)

            env.time = round(time, 1)

            if data_manager.isEvaluationIntervalCompleted(env.time, evaluationInterval):

                # compute the profits for each businessman
                for bm in stillALiveBms:

                    for company in bm.companies:
                        nProfit = company.computeNettoProfit()                        
                        company.computeCompanyValue()

                    # compute the updated capital for the businessman and print
                    bm.capital += nProfit + bm.subsidiaries

                averageCompany = env.computeAverageCompanyValue()
                env.government.regulate(env.avgCapital, averageCompany, stillALiveBms)
                env.computeAvgCapital()
                env.computeAvgHappiness()
                data_manager.evaluateStats(time, env.listOfPeople)

    # plot profit history and capital
    data_manager.exportToCSV()
    data_manager.writeToJson(data_manager.FileType.RESULTS, env)


def create_new_environment():
    data_manager.init_statistics()
    env = Environment()
    jsonfile = data_manager.FileType.CONFIG
    data_manager.writeToJson(jsonfile, env)
    return jsonfile

def use_existing_environment():
    dataframe = pd.read_csv(data_manager.FileType.STATS.value, index_col=0)
    lastItem = dataframe.tail(1)
    lastDfIndex = lastItem.index.item() + 1
    lastDate = data_manager.convertStringToDate(lastItem.time.item())
    data_manager.init_statistics(dataframe=dataframe,
                                 dfIdx=lastDfIndex,
                                 startDt=lastDate)
    return data_manager.FileType.RESULTS
    

if __name__ == "__main__":
    # SELECT THIS OPTION TO CREATE A NEW ENVIRONMENT
    jsonfile = create_new_environment()
    # SELECT THIS OPTION TO LOAD AN EXISTING ENVIRONMENT
    # jsonfile = use_existing_environment()
    runFromJson(jsonfile)