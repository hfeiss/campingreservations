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

#plt.style.use('ggplot')

plt.figure(figsize=(12, 8))    
ax = plt.subplot(111)    

plt.yticks(range(0, 7000001, 1000000), [str(x) + " Million" for x in range(0, 8)], fontsize=14)    
plt.xticks(fontsize=14)

ax.spines["top"].set_visible(False)    
ax.spines["bottom"].set_visible(False)    
ax.spines["right"].set_visible(False)    
ax.spines["left"].set_visible(False) 

plt.ylim(-200000, 7000000)    
plt.xlim(-.25, 16)
plt.xlabel('Number of Nights', fontsize = 14)
plt.title('Number of Reservations by Length of Stay', fontsize = 20)

plt.bar(data['LengthOfStay'], data['count(LengthOfStay)'])
plt.tight_layout()
plt.savefig(imagepath + '/histOfNights.png')