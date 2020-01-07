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
for root, dirs, file in os.walk(cleanpath + 'CountsOfNights/'):
    list_years.extend(file)
list_years.sort()

# Create and clean dataframe from list of .pkl s
data = pd.DataFrame()
data['count(LengthOfStay)'] = 0
for file in list_years:
    df = pd.read_pickle(cleanpath + 'CountsOfNights/' + file)
    df.fillna(0, inplace = True)
    #data['count(LengthOfStay)'] += df['count(LengthOfStay)']
    data = pd.concat([data, df], sort = True)

data = data.groupby('LengthOfStay').sum().reset_index()
data = data[data['LengthOfStay'] > 0]
data.reset_index(inplace = True, drop = True)
print(data.columns)

plt.bar(data['LengthOfStay'], data['count(LengthOfStay)'])
plt.savefig(imagepath + '/histOfNights.png')