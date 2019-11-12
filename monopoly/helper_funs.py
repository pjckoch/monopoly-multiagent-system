import government
import businessman
import company

def transaction(sender, receiver, amount):
    if type(sender) is businessman.Businessman:
        sender.capital -= amount
    elif type(sender) is government.Government:
        sender.governmentMoney -= amount
    if type(receiver) is company.Company:
        receiver.turnOver += 2*amount
    elif type(receiver) is government.Government:
        receiver.governmentMoney += amount
    else:
        receiver.capital += amount