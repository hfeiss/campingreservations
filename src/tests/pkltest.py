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


def test_pkl(path):
    print(pd.read_pickle(cleanpath + path))


if __name__ == '__main__':
    pklchoice = 'DistanceByFacilityState/2016.pkl'
    test_pkl(pklchoice)
