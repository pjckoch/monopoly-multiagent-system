import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import CheckButtons
from matplotlib.widgets import TextBox
import numpy as np


pause_interval = 0.1


fig = plt.figure('Monopoly')
ax1 = fig.add_subplot(2,1,1, adjustable='box', aspect=.5)
ax1.set_title('Capital Distribution')

ax2 = fig.add_subplot(2,1,2)
ax2.set_title('Profit History')
ax2.set_xlabel('Time (days)')
ax2.set_ylabel('Profit (USD)')

initial_text = ""
active = []
currentDay = 0

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
    l2 = []

    def update(day):

        global currentDay

        currentDay = day

        ax1.clear()
        ax2.clear()
        # labels = [('BM' + str(bm.id)) for bm in businessmen]
        l1 = ax1.pie(capitalArr[:,day], autopct= lambda p: int(p/100.*capitalArr[:,day].sum()), shadow=True, startangle=90, colors=colors)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax1.set_title('Capital Day ' + str(day+1))

        for j, clr in zip(range(len(bmIds)), colors):
            l, = ax2.plot(days[0:day], totalDailyProfits[j, 0:day], color=clr, label=j)
            l2.append(l)

            if l.get_label() not in active:
                l.set_visible(False)
            else:
                l.set_visible(True)

        fig.legend([l1, l2],     # The line objects
           labels=line_labels,   # The labels for each line
           loc="upper right",    # Position of legend
           borderaxespad=0.1,    # Small spacing around legend box
           title="Businessmen"  # Title for the legend
        )

        plt.pause(pause_interval)


    def submit(text):
        global active
        if text == "all":
            active = []
            for bm in bmIds:
                active.append(str(bm))
        elif text == "none":
                active = []
        elif text not in active:
                active.append(text)
        else: 
            active.remove(text)
            
        global currentDay

        if currentDay == numDays - 1:
            update(numDays-1)
            
        

    anim = FuncAnimation(fig, update, frames=range(numDays), repeat=False)
    axbox = plt.axes([0.125, 0.5, 0.1, 0.075])
    text_box = TextBox(axbox, 'BM no:', initial=initial_text)
    text_box.on_submit(submit)

    plt.show()