import pandas as pd
from enum import Enum
import pandas as pd
import datetime
import json

import company
import environment
import businessman
import government


df_total = None
dfIndex = None
startDate = None
currentDate = None


class EvaluationInterval(Enum):
    ANNUAL = "annual"
    MONTHLY = "monthly"
    DAILY = "daily"

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

class FileType(Enum):
    CONFIG = "config.json"
    RESULTS = "results.json"
    STATS = "statistics.csv"

class JsonEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, Enum):
                return obj.name  # Could also be obj.value
            elif isinstance(obj, environment.Environment):
                return {
                    '__class__': 'Environment',
                    '__value__': obj.__dict__
                }
            elif isinstance(obj, businessman.Businessman):
                return {
                    '__class__': 'Businessman',
                    '__value__': obj.__dict__
                }
            elif isinstance(obj, company.Company):
                return {
                    '__class__': 'Company',
                    '__value__': obj.__dict__
                }
            elif isinstance(obj, government.Government):
                return {
                    '__class__': 'Government',
                    '__value__': obj.__dict__
                }
            return obj.__dict__

def init_statistics(dataframe=None,
                    dfIdx=0,
                    startDt=datetime.date(2019,1,1)):
                    global df_total, dfIndex, startDate, currentDate
                    df_total = pd.DataFrame() if dataframe is None else dataframe
                    dfIndex = dfIdx
                    startDate = startDt
                    currentDate = startDate
    

def writeToJson(filepath, data):
    with open(filepath.value, 'w') as f:
        json.dump(data, f, cls = JsonEncoder, indent=4)
        f.close()

def readFromJson(filepath):
    with open(filepath.value, 'r') as f:
        data = json.loads(f.read(), object_hook=deserialize_objects)
        f.close()
    return data

def exportToCSV():
    df_total.to_csv(FileType.STATS.value)

def getTime(days):
    global startDate
    return startDate + datetime.timedelta(days=days)

def convertStringToDate(datestr):
    return datetime.datetime.strptime(datestr, '%Y-%m-%d').date()

def isEvaluationIntervalCompleted(days, evaluationInterval):
    global currentDate, startDate
    oldDate = currentDate
    currentDate = startDate + datetime.timedelta(days=days)
    if evaluationInterval == EvaluationInterval.DAILY and days % 1.0 == 0.0:
        return True
    elif evaluationInterval == EvaluationInterval.MONTHLY:
        if oldDate.month != currentDate.month or oldDate.year != currentDate.year:
            # the part after the OR is for the case that the evaluation interval is changed in a step-by-step run process
            return True
    elif evaluationInterval == EvaluationInterval.ANNUAL:
        if oldDate.year != currentDate.year:
            return True
    else:
        return False

def evaluateStats(time, listOfPeople):
    """Evaluate the stats for a list of businessmen over a given evaluation interval"""
    time = getTime(days=time)
    for bm in listOfPeople:
        turnOver, taxes, nettoProfit = computeStatsForEvaluationInterval(bm)
        appendToDataFrame(time, bm, turnOver, taxes, nettoProfit)

def computeStatsForEvaluationInterval(bm):
    """Compute the stats for one Businessman over a given evaluation interval"""
    turnOver = 0
    taxes = 0
    nettoProfit = 0

    for comp in bm.companies:
        turnOver += comp.turnOverHistory[-1]
        taxes += comp.taxHistory[-1]
        nettoProfit += comp.nettoProfitHistory[-1]
        
    return turnOver, taxes, nettoProfit

def appendToDataFrame(time, bm, turnOver, taxes, nettoProfit):
    """Function to append a stats for a certain businessman to a given dataframe"""
    global dfIndex, df_total

    numOfMedicals = sum(1 for comp in bm.companies if comp.category == company.BusinessCategory.MEDICAL)
    numOfSupermarkets = sum(1 for comp in bm.companies if comp.category == company.BusinessCategory.SUPERMARKET)
    numOfRestaurants = sum(1 for comp in bm.companies if comp.category == company.BusinessCategory.RESTAURANT)
    numOfEntertainments = sum(1 for comp in bm.companies if comp.category == company.BusinessCategory.ENTERTAINMENT)
    numOfLuxuries = sum(1 for comp in bm.companies if comp.category == company.BusinessCategory.LUXURY)

    df_part = pd.DataFrame({"time": time,
                       "id": bm.id,
                       "numOfCompanies": len(bm.companies),
                       "numOfMedicals": numOfMedicals,
                       "numOfSupermarkets": numOfSupermarkets,
                       "numOfRestaurants": numOfRestaurants,
                       "numOfEntertainments": numOfEntertainments,
                       "numOfLuxuries": numOfLuxuries,
                       "turnOver": turnOver,
                       "taxes": taxes,
                       "nettoProfit": nettoProfit,
                       "subsidiaries": bm.subsidiaries,
                       "capital": bm.capital,
                       "happiness": bm.happiness},
                       index = [dfIndex])
    df_total = df_total.append(df_part, sort=False)
    dfIndex += 1


def deserialize_objects(obj):
    if '__class__' in obj:
        objval = obj['__value__']
        if obj['__class__'] == 'Company':
            des_obj = deserialize_company(objval) 
        elif obj['__class__'] == 'Businessman':
            des_obj = deserialize_businessman(objval)
        elif obj['__class__'] == 'Government':
            des_obj = deserialize_government(objval)
        elif obj['__class__'] == 'Environment':
            des_obj = deserialize_environment(objval)
    else:
        des_obj = obj
    return des_obj

def deserialize_businessman(obj):
    return businessman.Businessman(businessmanId = obj['id'],
                                   name = obj['name'],
                                   capital = obj['capital'],
                                   happiness = obj['happiness'],
                                   isAlive = obj['isAlive'],
                                   subsidiaries = obj['subsidiaries'],
                                   companiesList = obj['companies'])

def deserialize_company(obj):
    category = company.BusinessCategory[obj['category']]
    return company.Company(companyId = obj['id'],
                           name = obj['name'],
                           category = category,
                           frequency = obj['_frequency'],
                           necessity = obj['_necessity'],
                           price = obj['price'],
                           quality = obj['quality'],
                           turnOver = obj['turnOver'],
                           fixedCost = obj['fixedCost'],
                           variableCost = obj['variableCost'],
                           companyValue= obj['companyValue'],
                           investmentLevel = obj['investmentLevel'],
                           bruttoProfitHistory = obj['bruttoProfitHistory'],
                           nettoProfitHistory = obj['nettoProfitHistory'],
                           turnOverHistory = obj['turnOverHistory'],
                           taxHist = obj['taxHistory'])

def deserialize_government(obj):
    politics = None #government.PoliticsSwitcher[obj['politics']]
    return government.Government(politics=politics,
                                 taxesStatus=obj['taxesStatus'],
                                 subsidiariesStatus=obj['subsidiariesStatus'],
                                 taxRate=obj['taxRate'],
                                 subsidyValue=obj['subsidyValue'],
                                 governmentMoney=obj['governmentMoney'],
                                 startCompPrice=obj['startCompPrice'],
                                 investOwnCompPrice=obj['investOwnCompPrice'])

def deserialize_environment(obj):
    return environment.Environment(numPeople=obj['numPeople'],
                                   numCompanies=obj['numCompanies'],
                                   government=obj['government'],
                                   listPeople=obj['listOfPeople'],
                                   listCompanies=obj['listOfCompanies'],
                                   numActions=obj['numActions'],
                                   suicideCount=obj['suicideCount'],
                                   time=obj['time'])