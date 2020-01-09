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

pklchoice = 'DistanceByFacilityState/2016.pkl'
df = pd.read_pickle(cleanpath + pklchoice)
print(df)
