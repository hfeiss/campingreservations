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
    df.drop(['BoatTrailer', 'PowerBoat', 'CanoeKayak'], axis = 1, inplace = True)

    # sum types of RVs
    df['RV'] = df['RVMotorhome'] + df['FifthWheel']
    df.drop(['FifthWheel', 'RVMotorhome'], axis = 1, inplace = True)

    # sum types of cars
    df['Car'] = df['Car'] + df['Van']
    df.drop(['Van'], axis = 1, inplace = True)
    

    # normalize to percents
    df = df.div(df.sum(axis = 1), axis = 0)
    
    # add year to df
    df['Year'] = int(time)
    
    # add year to data dataframe
    data = pd.concat([data, df])

data.reset_index(inplace = True)
print(data)
print(data.columns)
