import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.animation import FuncAnimation
import numpy as np


pause_interval = 0.1


fig = plt.figure('Monopoly')
ax1 = fig.add_subplot(2,1,1, adjustable='box', aspect=.5)
ax1.set_title('Capital Distribution')

ax2 = fig.add_subplot(2,1,2)
ax2.set_title('Profit History')
ax2.set_xlabel('Time (days)')
ax2.set_ylabel('Profit (USD)')

def plot_all(peopleCapitalDict, peopleProfitDict, numDays):

    bmIds = list(peopleProfitDict.keys())
    line_labels = ['BM ' + str(id) for id in bmIds]

    ax2.set_xlim([1, numDays])
    ax2.set_ylim([-1000, 3000])

    capitalList = list(peopleCapitalDict.values())
    capitalArr = np.array(capitalList)


    profitList = list(peopleProfitDict.values())
    profitArr = np.array(profitList)[bmIds]
    totalDailyProfits = np.sum(profitArr, 2)
    colors = cm.gnuplot(np.linspace(0.1, 0.8, len(bmIds)))

    days = np.arange(1, numDays + 1)

    def update(day):


        ax1.clear()
        # labels = [('BM' + str(bm.id)) for bm in businessmen]
        l1 = ax1.pie(capitalArr[:,day], autopct= lambda p: int(p/100.*capitalArr[:,day].sum()), shadow=True, startangle=90, colors=colors)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax1.set_title('Capital Day ' + str(day+1))

        for j, clr in zip(range(len(bmIds)), colors):
            l2 = ax2.plot(days[:day+1], totalDailyProfits[j, :day+1], color=clr, label=j)


        fig.legend([l1, l2],     # The line objects
           labels=line_labels,   # The labels for each line
           loc="upper right",    # Position of legend
           borderaxespad=0.1,    # Small spacing around legend box
           title="Businessmen"  # Title for the legend
        )

        plt.pause(pause_interval)



    anim = FuncAnimation(fig, update, frames=range(numDays), repeat=False)   
    plt.show()