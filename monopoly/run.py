import numpy as np
import pandas as pd
import random
import logger
from environment import Environment
from government import PoliticsSwitcher
from plot_history import *
from enum import Enum
import data_manager
import argparse
import helper_funs as hf

log_once = False
append = False
clearLogCount = 0
yearCount = 0

days = 365
evaluationInterval = data_manager.EvaluationInterval.MONTHLY

parser = argparse.ArgumentParser(description='Run the multiagent monopoly system.')
parser.add_argument('-e', '--existing', help='Use existing environment')

def runFromJson(jsonFile):
    global log_once
    global append
    global clearLogCount
    global yearCount
    env = data_manager.readFromJson(jsonFile)
    env.applyInflation(0.0)

    for time in np.linspace(0.0, days, num = env.numActions * days + 1):
        # we don't need to round here, we only want to exclude the very first value
        if time != 0.0:

            for bm in env.listOfPeople:
                action = bm.chooseAction(env.listOfCompanies, env)
                # assuming buying a new company counts as an investment
                bm.invest(env)
                # for company in hf.get_companies_of_bm(bm,env):
                    # company.bankrupcy(env)

            # Elections
            if env.time % 365 == 0:
                print("")
                env.government.politics = PoliticsSwitcher.NEUTRAL
                # n = random.randint(1,3)
                # if n == 1:
                #     env.government.politics = PoliticsSwitcher.SOCIALIST
                #     logger.log_government(time, "SOCIALIST")
                #     print("SOCIALIST")
                # elif n == 2:
                #     env.government.politics = PoliticsSwitcher.NEUTRAL
                #     logger.log_government(time, "NEUTRAL")
                #     print("NEUTRAL")
                # elif n == 3:
                #     env.government.politics = PoliticsSwitcher.LIBERAL
                #     logger.log_government(time, "LIBERAL")
                #     print("LIBERAL")

            env.time = round(time, 1)

            if data_manager.isEvaluationIntervalCompleted(env.time, evaluationInterval):
                env.totalMoney = 0
                # compute the profits for each businessman
                for bm in env.listOfPeople:
                    env.totalMoney += bm.capital
                    nProfit = 0
                    for company in hf.get_companies_of_bm(bm, env):
                        env.totalMoney += company.turnOver
                        logger.log_company_stats(env.time, company, log_once)
                        bProfit = company.computeBruttoProfit()
                        company.payCosts(env.government)
                        env.government.regulateTax(bm, company, env.time)
                        nProfit += company.computeNettoProfit()
                        company.computeCompanyValue()
                        company.updateSale()        # update the "memory" that prevents the BM to buy/sell the same company over and over
                    bm.actionHistory.append(bm.actionCounter)
                    bm.actionCounter = 0
                    # add the summed up netto profits to the businessman capital
                    bm.capital += nProfit
                    bm.incomeHistory.append(nProfit)

                log_once = True
                env.totalMoney += env.government.governmentMoney
                logger.log_split(env.time)
                averageCompany = env.computeAverageCompanyValue()
                env.government.regulate(env.listOfPeople)
                env.computeAvgCapital()
                env.computeAvgHappiness()
                data_manager.evaluateStats(time, env)

    annual_incomes = hf.get_annual_incomes(env.listOfPeople)
    print("Gini Coefficient: " + str(hf.gini(annual_incomes)))
    data_manager.exportToCSV()
    data_manager.writeToJson(data_manager.FileType.RESULTS, env)


def create_new_environment():
    data_manager.init_statistics()
    env = Environment()
    jsonfile = data_manager.FileType.CONFIG
    data_manager.writeToJson(jsonfile, env)
    return jsonfile

def use_existing_environment():
    logger.change_write_mode_to_append()
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
        append = True
    else:
        env_type = 'new'
    jsonfile = chooseEnvironment[env_type]()
    runFromJson(jsonfile)