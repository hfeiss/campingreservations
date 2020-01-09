from dataclass import *
import os

# Create filepaths within df directory
srcpath = os.path.split(os.path.abspath(''))[0]
rootpath = os.path.split(srcpath)[0]
datapath = os.path.join(rootpath, 'data')
rawpath = os.path.join(datapath, 'raw')
respath = os.path.join(rawpath, 'reservations_rec_gov/')
cleanpath = os.path.join(datapath, 'cleaned/')

def make_pkls(sourcepath, operation, years = None):
    '''
    Input
    sourcepath: path to a directory containing .csv files
    operation: Data.method
    years: (optional) defaults to all files in sourcepath

    Actions
    Creates a Data object
    Performs Data.operation on each file
    
    Output
    Saves a .plk in at .folder of the operation in cleanpath
    '''
    list_years = []
    if years:
        list_years = years
    else:
        for root, dirs, file in os.walk(sourcepath):
            list_years.extend(file)
    list_years.sort()

    for year in list_years:
        df = Data(sourcepath + year)
        Data.clean(df)
        operation(df)
        df.write_to_pkl(cleanpath
                        + df.folder
                        + year[:-4] 
                        + '.pkl')
        print(f'Wrote {str(year[:-4])} in {df.folder}')

if __name__ == '__main__':
    '''
    +++++++++++++++++++++++++++++++++++++++++++++++++++
    This is about 80 hours of computation for all years
    +++++++++++++++++++++++++++++++++++++++++++++++++++
    '''
    #make_pkls(respath, Data.make_DistanceByCustomerState, years=years_left)
    #make_pkls(respath, Data.make_DistanceByCustomerZIP)
    make_pkls(respath, Data.make_DistanceByFacilityState)
    #make_pkls(respath, Data.make_DistanceByFacilityZIP)
    #make_pkls(respath, Data.make_DistanceByWeekend)
    #make_pkls(respath, Data.make_DistanceByLonger)
    #make_pkls(respath, Data.make_SumOfCategories)
    #make_pkls(respath, Data.make_CountsOfNights)