import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

def plotProfitHistory(peopleProfitDict, bmIds, numDays):

    plt.figure('Profit History')
    plt.axis([0, numDays, -2000, 2000])
    # plt.axes().spines['bottom'].set_position(('data', 0))
    plt.title('Profit History for Businessmen ' + str(bmIds))
    plt.xlabel('Time (days)')
    plt.ylabel('Profit (USD)')


    profitList = list(peopleProfitDict.values())
    profitList = [profitList[bmId] for bmId in bmIds]
    profitArr = np.array(profitList)
    totalDailyProfits = np.sum(profitArr, 2)
    
    profits = [[], [], []]
    days = []

    colors = cm.rainbow(np.linspace(0, 1, len(bmIds)))

    for day in range(int(numDays)):
        #print(totalDailyProfits[:, day])
        days.append(day + 1)

        for i, clr in zip(range(len(bmIds)), colors):
            profits[i].append(totalDailyProfits[i, day])
            plt.plot(days, profits[i], color=clr)

        plt.pause(0.1)

    plt.show()