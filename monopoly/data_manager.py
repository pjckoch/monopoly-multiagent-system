import pandas as pd
from enum import Enum
from company import BusinessCategory
import pandas as pd
import datetime

filepath = ("statistics.csv")
df_total = pd.DataFrame()
dfIndex = 0
startYear = 2019

def exportToCSV():
    
    df_total.to_csv(filepath)

def evaluateStats(time, evaluationInterval, listOfPeople):
    time = int(time//evaluationInterval.value)
    if evaluationInterval == EvaluationInterval.MONTHLY:
        year = int((time-1) // 12)
        month = Month(time - 12 * year).value
        time = datetime.datetime(year+startYear, month, 1)
    elif evaluationInterval == EvaluationInterval.YEARLY:
        time = datetime.datetime(year+startYear, 12, 31)
    
    for bm in listOfPeople:
        profit = 0
        for comp in bm.companies:
            profit += sum(comp.profitHistory[-evaluationInterval.value:])
        appendToDataFrame(time, bm, profit)

def appendToDataFrame(time, bm, profit):
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
                       "profit": profit,
                       "subsidiaries": bm.subsidiaries,
                       "capital": bm.capital,
                       "happiness": bm.happiness},
                       index = [dfIndex])
    df_total = df_total.append(df_part)
    dfIndex += 1


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
