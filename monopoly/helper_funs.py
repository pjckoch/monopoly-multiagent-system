import government
import businessman
import company
import numpy as np

def transaction(sender, receiver, amount):
    if type(sender) is businessman.Businessman:
        sender.capital -= amount
    elif type(sender) is government.Government:
        sender.governmentMoney -= amount
    if type(receiver) is company.Company:
        receiver.turnOver += amount
    elif type(receiver) is government.Government:
        receiver.governmentMoney += amount
    else:
        receiver.capital += amount


def get_companies_of_bm(bm, env):
    bmCompIds = [comp.id for comp in bm.companies]
    return [comp for comp in env.listOfCompanies if comp.id in bmCompIds]

def get_annual_incomes(listOfBms):
    incomes = []
    for bm in listOfBms:
        annual_income = np.sum(bm.incomeHistory[-12:]) + np.sum(bm.subsidiariesHistory[-12:])
        incomes.append(annual_income)
    return incomes

def gini(x):
    # Mean absolute difference
    mad = np.abs(np.subtract.outer(x, x)).mean()
    # Relative mean absolute difference
    rmad = mad/np.mean(x)
    # Gini coefficient
    g = 0.5 * rmad
    return g

        