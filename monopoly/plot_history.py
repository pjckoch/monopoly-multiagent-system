import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import CheckButtons
from matplotlib.widgets import TextBox
from company import BusinessCategory
import numpy as np


pause_interval = 0.05


fig = plt.figure('Monopoly')
ax1 = fig.add_subplot(3,1,1, adjustable='box', aspect=.5, position=[0,0.7,0.2,0.2])
ax1.set_title('Capital Distribution')

ax2 = fig.add_subplot(3,1,2, position=[0.1,0.35,0.3,0.2])
ax2.set_title('BM\'s Profit History')
ax2.set_xlabel('Time (days)')
ax2.set_ylabel('Profit (USD)')

ax3 = fig.add_subplot(3,1,2, position=[0.6,0.35,0.3,0.2])
ax3.set_title('Company\'s Profit History')
ax3.set_xlabel('Time (days)')
ax3.set_ylabel('Profit (USD)')

initial_text = ""
active1 = []
active2 = []
currentDay = 0

def plot_all(peopleCapitalDict, peopleProfitDict, companiesProfitDict, companiesTypeIds, numDays):

    bmIds = list(peopleProfitDict.keys())
    line_labels = ['BM ' + str(id) for id in bmIds]

    cmpIds = list(companiesProfitDict.keys())
    line_labels = ['BM ' + str(id) for id in cmpIds]

    ax2.set_xlim([1, numDays])
    ax2.set_ylim([-1000, 3000])

    capitalList = list(peopleCapitalDict.values())
    capitalArr = np.array(capitalList)


    profitList = list(peopleProfitDict.values())
    profitArr = np.array(profitList)[bmIds]
    totalDailyProfits = np.sum(profitArr, 2)
    colors1 = cm.gnuplot(np.linspace(0.1, 0.8, len(bmIds)))
    
    cmpList = list(companiesProfitDict.values())
    dailyCmpProfits = np.array(cmpList)[cmpIds]
    colors2 = cm.gnuplot(np.linspace(0.2, 0.9, len(cmpIds)))

    days = np.arange(1, numDays + 1)
    l2 = []
    l3 = []

    def update(day):

        global currentDay

        currentDay = day

        ax1.clear()
        ax2.clear()
        ax3.clear()
        # labels = [('BM' + str(bm.id)) for bm in businessmen]
        if len(bmIds) < 5:
            l1 = ax1.pie(capitalArr[:,day], autopct= lambda p: int(p/100.*capitalArr[:,day].sum()), shadow=True, startangle=90, colors=colors1)
        else:
            l1 = ax1.pie(capitalArr[:,day], autopct='', shadow=True, startangle=90, colors=colors1)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax1.set_title('Capital Day ' + str(day+1))

        for j, clr in zip(range(len(bmIds)), colors1):
            l, = ax2.plot(days[0:day], totalDailyProfits[j, 0:day], color=clr, label=j)
            l2.append(l)

            if l.get_label() not in active1:
                l.set_visible(False)
            else:
                l.set_visible(True)

        for i, clr in zip(range(len(cmpIds)), colors2):
            g, = ax3.plot(days[0:day], dailyCmpProfits[i, 0:day], color=clr, label=i)
            l3.append(l)

            if int(g.get_label()) not in active2:
                g.set_visible(False)
            else:
                g.set_visible(True)

        fig.legend([l1, l2],     # The line objects
           labels=line_labels,   # The labels for each line
           loc="upper right",    # Position of legend
           borderaxespad=0.1,    # Small spacing around legend box
           title="Businessmen"  # Title for the legend
        )

        plt.pause(pause_interval)


    def submit1(text):
        global active1
        if text == "all":
            active1 = []
            for bm in bmIds:
                active1.append(str(bm))
        elif text == "none":
            active1 = []
        elif text not in active1:
                active1.append(text)
        else: 
            active1.remove(text)
            
        global currentDay

        if currentDay == numDays - 1:
            update(numDays-1)
            
    def submit2(text):
        global active2
        print(companiesTypeIds)
        key = text.upper()
        if key in companiesTypeIds:
            active2 = companiesTypeIds[text.upper()]
            print(active2)
        else:
            active2 = []

    anim = FuncAnimation(fig, update, frames=range(numDays), repeat=False)
    axbox1 = plt.axes([0.1, 0.58, 0.1, 0.075])
    text_box1 = TextBox(axbox1, 'BM no:', initial=initial_text)
    text_box1.on_submit(submit1)

    axbox2 = plt.axes([0.6, 0.58, 0.1, 0.075])
    text_box2 = TextBox(axbox2, 'Category:', initial=initial_text)
    text_box2.on_submit(submit2)

    plt.show()