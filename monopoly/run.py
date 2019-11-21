import numpy as np
import pandas as pd
import random
import logger
from environment import Environment
from plot_history import *
from enum import Enum
import data_manager
import argparse

days = 365
evaluationInterval = data_manager.EvaluationInterval.MONTHLY

parser = argparse.ArgumentParser(description='Run the multiagent monopoly system.')
parser.add_argument('-e', '--existing', help='Use existing environment')

def runFromJson(jsonFile):

    env = data_manager.readFromJson(jsonFile)

    totalMoney = 0
    for time in np.linspace(0.0, days, num = env.numActions * days + 1):
        totalMoney = 0
        # we don't need to round here, we only want to exclude the very first value
        if time != 0.0:

            stillALiveBms = [bm for bm in env.listOfPeople if bm.isAlive]

            activeCompanies = []


            env.updateActiveCompanies()

            money = 0

            for bm in stillALiveBms:
                money += bm.capital
                action = bm.chooseAction(env.activeCompanies, env)
                # assuming buying a new company counts as an investment
                bm.invest(env)
                totalMoney += bm.capital
                for company in bm.companies:
                    company.updateSale()
                    company.bankrupcy(env)

            env.updateActiveCompanies()

            money += env.government.governmentMoney
            print(money)


            env.time = round(time, 1)

            if data_manager.isEvaluationIntervalCompleted(env.time, evaluationInterval):
                # compute the profits for each businessman
                for bm in stillALiveBms:
                    logger.log_businessman_sales(days, bm)
                    # env.inflationInDaHouse(bm)
                    print("Businessman ID:" + str(bm.id))
                    print("List of Sales:")
                    for company in bm.companies:
                        print(company.companySales)
                        company.companySales = []
                    nProfit = 0
                    for company in bm.companies:
                        logger.log_company_sales(env.time, company)
                        bProfit = company.computeBruttoProfit()
                        #QUICKFIX
                        env.government.regulateTax(bm, company)
                        nProfit += company.computeNettoProfit()         
                        # company.payCosts(env.government)            
                        company.computeCompanyValue()

                    # add the summed up netto profits to the businessman capital
                    bm.capital += nProfit

                logger.log_split(env.time)
                averageCompany = env.computeAverageCompanyValue()
                env.government.regulate(stillALiveBms)
                env.computeAvgCapital()
                env.computeAvgHappiness()
                data_manager.evaluateStats(time, env)

            totalMoney += env.government.governmentMoney
            # print("Day " + str(env.time) + ": " + str(totalMoney))

    data_manager.exportToCSV()
    data_manager.writeToJson(data_manager.FileType.RESULTS, env)


def create_new_environment():
    data_manager.init_statistics()
    env = Environment()
    jsonfile = data_manager.FileType.CONFIG
    data_manager.writeToJson(jsonfile, env)
    return jsonfile

def use_existing_environment():
    dataframe_total = pd.read_csv(data_manager.FileType.STATS.value, index_col=0)
    lastItem_total = dataframe_total.iloc[-1]
    lastDfIndex_total = len(dataframe_total.index) + 1
    lastDate = data_manager.convertStringToDate(lastItem_total.time)

    dataframe_companies = pd.read_csv(data_manager.FileType.COMPANY_STATS.value, index_col=0)
    lastItem_companies = dataframe_companies.tail(1)
    lastDfIndex_companies = len(lastItem_companies.index) + 1

    data_manager.init_statistics(dataframe_total=dataframe_total,
                                 dataframe_categories=dataframe_companies,
                                 dfIdx=lastDfIndex_total,
                                 dfIdxCompanies=lastDfIndex_companies,
                                 startDt=lastDate)
    return data_manager.FileType.RESULTS


chooseEnvironment = {
    'new': create_new_environment,
    'existing': use_existing_environment
}

if __name__ == "__main__":
    args = parser.parse_args()
    if args.existing:
        env_type = 'existing'
    else:
        env_type = 'new'
    jsonfile = chooseEnvironment[env_type]()
    runFromJson(jsonfile)