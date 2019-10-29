import pandas as pd
from enum import Enum
from company import BusinessCategory
import pandas as pd
import datetime
import json


filepath = ("statistics.csv")
df_total = pd.DataFrame()
dfIndex = 0
startYear = 2019

class EvaluationInterval(Enum):
    ANNUAL = 365
    MONTHLY = 30
    DAILY = 1

class Month(Enum):
    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12

class JsonEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, Enum):
                return obj.name  # Could also be obj.value
            return obj.__dict__

def writeToJson(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, cls = JsonEncoder, indent=4)
        f.close()

def readFromJson(filepath):
    with open(filepath, 'r') as f:
        data = json.loads(f, object_hook= JSONObject)
        f.close()
    return data

def exportToCSV():
    
    df_total.to_csv(filepath)

def evaluateStats(time, evaluationInterval, listOfPeople):
    """Evaluate the stats for a list of businessmen over a given evaluation interval"""
    time = int(time//evaluationInterval.value)
    if evaluationInterval == EvaluationInterval.MONTHLY:
        year = int((time-1) // 12)
        month = Month(time - 12 * year).value
        time = datetime.datetime(year+startYear, month, 1)
    elif evaluationInterval == EvaluationInterval.YEARLY:
        time = datetime.datetime(year+startYear, 12, 31)
    for bm in listOfPeople:
        turnOver, nettoProfit = computeStatsForEvaluationInterval(evaluationInterval, bm)
        appendToDataFrame(time, bm, turnOver, nettoProfit)

def computeStatsForEvaluationInterval(evaluationInterval, bm):
    """Compute the stats for one Businessman over a given evaluation interval"""
    nettoProfit = 0
    turnOver = 0

    for comp in bm.companies:
        turnOver = comp.turnOverHistory[-1]
        nettoProfit = comp.nettoProfitHistory[-1]
    #     # some profit and turnover to get total within the specified evaluationInterval
    #     nettoProfit += sum(comp.nettoProfitHistory[-evaluationInterval.value:])
    #     turnOver += sum(comp.turnOverHistory[-evaluationInterval.value:])
    return turnOver, nettoProfit

def appendToDataFrame(time, bm, turnOver, nettoProfit):
    """Function to append a stats for a certain businessman to a given dataframe"""
    global dfIndex, df_total

    numOfMedicals = sum(1 for comp in bm.companies if comp.category == BusinessCategory.MEDICAL)
    numOfSupermarkets = sum(1 for comp in bm.companies if comp.category == BusinessCategory.SUPERMARKET)
    numOfRestaurants = sum(1 for comp in bm.companies if comp.category == BusinessCategory.RESTAURANT)
    numOfEntertainments = sum(1 for comp in bm.companies if comp.category == BusinessCategory.ENTERTAINMENT)
    numOfLuxuries = sum(1 for comp in bm.companies if comp.category == BusinessCategory.LUXURY)

    df_part = pd.DataFrame({"time": time,
                       "id": bm.id,
                       "numOfCompanies": len(bm.companies),
                       "numOfMedicals": numOfMedicals,
                       "numOfSupermarkets": numOfSupermarkets,
                       "numOfRestaurants": numOfRestaurants,
                       "numOfEntertainments": numOfEntertainments,
                       "numOfLuxuries": numOfLuxuries,
                       "turnOver": turnOver,
                       "nettoProfit": nettoProfit,
                       "subsidiaries": bm.subsidiaries,
                       "capital": bm.capital,
                       "happiness": bm.happiness},
                       index = [dfIndex])
    df_total = df_total.append(df_part)
    dfIndex += 1
