import pandas as pd
import numpy as np
import os

# Create filepaths within df directory
srcpath = os.path.split(os.path.abspath(''))[0]
rootpath = os.path.split(srcpath)[0]
datapath = os.path.join(rootpath, 'data/')
rawpath = os.path.join(datapath, 'raw/')
respath = os.path.join(rawpath, 'reservations_rec_gov/')
cleanpath = os.path.join(datapath, 'cleaned/')
weekendpath = os.path.join(cleanpath, 'DistanceByWeekend/WithAK/')
longerpath = os.path.join(cleanpath, 'DistanceByLonger/WithAK/')

list_years = []
for root, dirs, file in os.walk(weekendpath):
    list_years.extend(file)
list_years.sort()

# throw out 2006, 2007 as outliers
list_years = list_years[2:]
weekend_avgs = []
longer_avgs = []
for year in list_years:
    longer = pd.read_pickle(longerpath + year)
    longer_avgs.append(longer['avg(DistanceTraveled)'][0])
    weekend = pd.read_pickle(weekendpath + year)
    weekend_avgs.append(weekend['avg(DistanceTraveled)'][0])
    
class WeekendLonger(object):

    def __init__(self):

        self.weekend_avg = np.average(weekend_avgs)
        self.weekend_std = np.std(weekend_avgs) * np.sqrt(len(weekend_avgs))
        
        self.longer_avg = np.average(longer_avgs)
        self.longer_std = np.std(longer_avgs) *  np.sqrt(len(longer_avgs))

if __name__ == '__main__':

    info = WeekendLonger()
    print(info.weekend_avg)


