import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

def plotProfitHistory(peopleProfitDict, bmIds, numDays):

    plt.figure('Profit History')
    plt.axis([0, numDays, -2000, 5000])
    # plt.axes().spines['bottom'].set_position(('data', 0))
    plt.title('Profit History for Businessmen ' + str(bmIds))
    plt.xlabel('Time (days)')
    plt.ylabel('Profit (USD)')


    profitList = list(peopleProfitDict.values())
    #profitList = [profitList[bmId] for bmId in bmIds]
    profitArr = np.array(profitList)[bmIds]
    print(profitArr)
    totalDailyProfits = np.sum(profitArr, 2)

    days = np.arange(1, numDays + 1)    # arange does not include the last value --> therefore + 1
    colors = cm.rainbow(np.linspace(0, 1, len(bmIds)))

    for day in days:

        for i, clr in zip(range(len(bmIds)), colors):
            plt.plot(days[0:day], totalDailyProfits[i, 0:day], color=clr, label=i)

        plt.pause(0.05)

    plt.show()


plt.figure('Capital History')
plt.axis([0, 50, 0, 20000])
plt.title('Capital History')
plt.xlabel('Time (days)')
plt.ylabel('Capital (USD)')
capitalHistory = [[], []]
clrs = cm.rainbow(np.linspace(0, 1, 2))


def plotCapitalHistory(capital, bmId, day):
    clr = clrs[bmId]
    capitalHistory[bmId].append(capital)
    days = range(day)
    plt.plot(days, capitalHistory[bmId], color=clr, label=str(bmId))