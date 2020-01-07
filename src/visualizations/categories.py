import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Create filepaths within df directory
srcpath = os.path.split(os.path.abspath(''))[0]
rootpath = os.path.split(srcpath)[0]
datapath = os.path.join(rootpath, 'data/')
cleanpath = os.path.join(datapath, 'cleaned/')
imagepath = os.path.join(rootpath, 'images/')

list_years = []
for root, dirs, file in os.walk(cleanpath + 'SumOfCategories/'):
    list_years.extend(file)
list_years.sort()

data = pd.DataFrame()
for file in list_years:
    time = file[:-4]
    df = pd.read_pickle(cleanpath + 'SumOfCategories/' + file)
    df.fillna(0, inplace = True)

    # sum types of tents
    df['Tent'] = df['Tent'] + df['SmallTent'] + df['LargeTentOver9x12']
    df.drop(columns=['SmallTent', 'LargeTentOver9x12'], axis = 1, inplace = True)
    
    # sum types of campers
    df['Camper'] = df['PickupCamper'] + df['Trailer'] + df['Popup']
    df.drop(['PickupCamper', 'Trailer', 'Popup'], axis = 1, inplace = True)

    # sum types of boats
    df['Watercraft'] = (df['BoatTrailer'] + df['PowerBoat']
                        + df['Boat'] + df['CanoeKayak'])
    df.drop(['BoatTrailer', 'PowerBoat', 'CanoeKayak', 'Boat'], axis = 1, inplace = True)

    # sum types of RVs
    df['RV'] = df['RVMotorhome'] + df['FifthWheel']
    df.drop(['FifthWheel', 'RVMotorhome'], axis = 1, inplace = True)

    # sum types of cars
    df['Car'] = df['Car'] + df['Van']
    df.drop(['Van'], axis = 1, inplace = True)
    

    # normalize to percents
    df = df.div(df.sum(axis = 1), axis = 0)
    df = df.div(0.01, axis = 0)
    
    # add year to df
    df['Year'] = int(time)
    
    # add year to data dataframe
    data = pd.concat([data, df])

data.reset_index(inplace = True)

tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),    
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),    
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),    
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),    
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

for i in range(len(tableau20)):    
    r, g, b = tableau20[i]    
    tableau20[i] = (r / 255., g / 255., b / 255.)

plt.figure(figsize=(12, 14))    

ax = plt.subplot(111)    
ax.spines["top"].set_visible(False)    
ax.spines["bottom"].set_visible(False)    
ax.spines["right"].set_visible(False)    
ax.spines["left"].set_visible(False) 

ax.get_xaxis().tick_bottom()    
ax.get_yaxis().tick_left()

plt.ylim(0, 75)    
plt.xlim(2005.5, 2019)


plt.yticks(range(0, 71, 10), [str(x) + "%" for x in range(0, 91, 10)], fontsize=14)    
plt.xticks(fontsize=14)


for y in range(10, 91, 10):    
    plt.plot(range(2005, 2019), [y] * len(range(2005, 2019)), "--", lw=0.5, color="black", alpha=0.3)

plt.tick_params(axis="both", which="both", bottom="off", top="off",    
                labelbottom="on", left="off", right="off", labelleft="on")

categories = ['RV', 'Tent', 'Camper', 'Watercraft', 'Car']

for rank, column in enumerate(categories):    
    # Plot each line separately with its own color, using the Tableau 20    
    # color set in order.    
    plt.plot(data.Year.values,    
            data[column.replace("\n", " ")].values,    
            lw=2.5, color=tableau20[rank])

plt.tight_layout()
plt.savefig(imagepath + 'categories.png')