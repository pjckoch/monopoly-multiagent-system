import pandas as pd
from enum import Enum
import pandas as pd
import datetime
import json

import company
import environment
import businessman
import government

filepath = ("statistics.csv")
categories_filepath = ("companiesStats.csv")
df_total = pd.DataFrame()
df_categories = pd.DataFrame()
dfIndex = 0
dfIndexCompanies = 0
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

def writeToJson(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, cls = JsonEncoder, indent=4)
        f.close()

def readFromJson(filepath):
    with open(filepath, 'r') as f:
        data = json.loads(f.read(), object_hook=deserialize_objects)
        f.close()
    return data

def exportToCSV():
    df_total.to_csv(filepath)
    df_categories.to_csv(categories_filepath)

def evaluateStats(time, evaluationInterval, listOfPeople):
    """Evaluate the stats for a list of businessmen over a given evaluation interval"""
    time = int(time//evaluationInterval.value)
    if evaluationInterval == EvaluationInterval.MONTHLY:
        year = int((time-1) // 12)
        month = Month(time - 12 * year).value
        time = datetime.datetime(year+startYear, month, 1)
    elif evaluationInterval == EvaluationInterval.ANNUAL:
        time = datetime.datetime(year+startYear, 12, 31)
    elif evaluationInterval == EvaluationInterval.DAILY:
        starttime = datetime.datetime(startYear, 1, 1)
        time = starttime + datetime.timedelta(days=time)
    for bm in listOfPeople:
        turnOver, taxes, nettoProfit = computeStatsForEvaluationInterval(evaluationInterval, bm)
        appendToDataFrame(time, bm, turnOver, taxes, nettoProfit)
        for cmp in bm.companies:
            #compute values??
            appendToDataFrameCategories(time, cmp, bm)


def computeStatsForEvaluationInterval(evaluationInterval, bm):
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
    df_total = df_total.append(df_part)
    dfIndex += 1

def appendToDataFrameCategories(time, company, owner):
    """Function to append a stats for businessess to a given dataframe"""
    global dfIndexCompanies, df_categories


    df_part = pd.DataFrame({"time": time,
                       "id": company.id,
                       "name": company.name,
                       "owner": owner.name,
                       "category": company.category,
                       "turnOver": company.turnOver,
                       #"taxes": company.taxes,
                       "companyValue": company.companyValue,
                       "fixedCost": company.fixedCost,
                       "variableCost": company.variableCost},
                       index = [dfIndexCompanies])

    df_categories = df_categories.append(df_part)
    dfIndexCompanies += 1



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
        obj.pop(des_obj)
        return des_obj

def deserialize_businessman(obj):
    return businessman.Businessman(businessmanId = obj['id'],
                                   name = obj['name'],
                                   capital = obj['capital'],
                                   happiness = obj['happiness'],
                                   isAlive = obj['isAlive'],
                                   subsidiaries = obj['subsidiaries'],
                                   companies = obj['companies'])

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
                           taxes = obj['taxes'],
                           companyValue= obj['companyValue'],
                           investmentLevel = obj['investmentLevel'],
                           bruttoProfitHistory = obj['bruttoProfitHistory'],
                           nettoProfitHistory = obj['nettoProfitHistory'],
                           turnOverHistory = obj['turnOverHistory'])

def deserialize_government(obj):
    politics = government.PoliticsSwitcher[obj['politics']]
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
                                   listOfPeople=obj['listOfPeople'],
                                   listOfCompanies=obj['listOfCompanies'],
                                   numActions=obj['numActions'],
                                   suicideCount=obj['suicideCount'],
                                   time=obj['time'])