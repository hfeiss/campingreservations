import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Create filepaths within df directory
srcpath = os.path.split(os.path.abspath(''))[0]
rootpath = os.path.split(srcpath)[0]
datapath = os.path.join(rootpath, 'data')
rawpath = os.path.join(datapath, 'raw')
respath = os.path.join(rawpath, 'reservations_rec_gov/')
cleanpath = os.path.join(datapath, 'cleaned/')

df2006 = pd.read_pickle(cleanpath + 'CountsOfNights/2018.pkl')
print(df2006)

'''
plt.bar(df2006['LengthOfStay'], df2006['avg(DistanceTraveled)'])
plt.tight_layout()
plt.savefig('this.png')
'''