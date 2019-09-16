import numpy as np
from environment import Environment

days = 2.0

if __name__ == "__main__":

    environment = Environment()

    # print businessmen id's
    print("Businessman IDs:")
    print([bm.id for bm in environment.listOfPeople])

    # print companies id's
    print("Company IDs:")
    print([company.id for company in environment.listOfCompanies])

    # print average capital and average happiness
    print("Average Capital:")
    print(environment.avgCapital)
    print("Average Happiness:")
    print(environment.avgHappiness)

    # simulate with dummy profits
    for time in np.linspace(0.0, days, num = environment.numActions * days + 1):

        stillALiveBms = [bm for bm in environment.listOfPeople if bm.isAlive]

        for bm in stillALiveBms:
            """bm.chooseAction()"""
            break

        environment.time = round(time, 1)
        print("Days passed: " + str(environment.time))

        if environment.time != 0 and environment.time % 1.0 == 0.0 :

            # compute the profits for each businessman
            for bm in stillALiveBms:

                dailyProfits = []

                for company in bm.companies:

                    """dailyProfits.append(company.computeProfit())"""
                    dailyProfits.append(np.random.randint(low = -1000, high = 1000))

                # append the new values into the peopleProfitDict
                environment.addProfitsForBM(bm.id, dailyProfits)

                # compute the updated capital for the businessman and print
                bm.capital += sum(dailyProfits)
                printmsg = "Businessman " + str(bm.id)
                printmsg += " capital after " + str(time) + " days: "
                printmsg += str(bm.capital)
                print(printmsg)

    # print the profit history for each businessman
    print("People Profit Dictionary after " + str(days) + " days:")
    print(environment.peopleProfitDict)
    print("COMPANY ID: ",environment.listOfCompanies[0].id)
    print("COMPANY frequency: ",environment.listOfCompanies[0].frequency)
    print("COMPANY necessity: " ,environment.listOfCompanies[0].necessity)
    print("COMPANY price: " ,environment.listOfCompanies[0].price)
    print("COMPANY variableCost: " ,environment.listOfCompanies[0].variableCost)
    print("COMPANY fixedCost: " ,environment.listOfCompanies[0].fixedCost)
