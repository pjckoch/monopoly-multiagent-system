import government
import businessman
import company

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
        