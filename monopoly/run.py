import numpy as np
from environment import Environment

days = 2

if __name__ == "__main__":

    environment = Environment()

    # print businessmen id's
    print("Businessman IDs:")
    print([bm.id for bm in environment.listOfPeople])

    # print companies id's
    print("Company IDs:")
    print([company.id for company in environment.listOfCompanies])
    
    # append some dummy profits to businessmen
    for _ in range(days):
        for bm in [bm for bm in environment.listOfPeople if bm.isAlive]:
            profit = np.random.randint(low = -1000, high = 1000)
            environment.peopleProfitDict[bm.id].append(profit)

    print("People Profit Dictionary after " + str(days) + " days:")
    print(environment.peopleProfitDict)


    # print average capital and average happiness
    print("Average Capital:")
    print(environment.avgCapital)
    print("Average Happiness:")
    print(environment.avgHappiness)
