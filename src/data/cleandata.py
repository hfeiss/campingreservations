from dataclass import *
import os

# Create filepaths within df directory
srcpath = os.path.split(os.path.abspath(''))[0]
rootpath = os.path.split(srcpath)[0]
datapath = os.path.join(rootpath, 'data')
rawpath = os.path.join(datapath, 'raw')
respath = os.path.join(rawpath, 'reservations_rec_gov/')
cleanpath = os.path.join(datapath, 'cleaned/')


if __name__ == '__main__':
    list_res = []
    for root, dirs, file in os.walk(respath):
        list_res.extend(file)
    list_res.sort()
    '''
    for year in list_res:
        df = Data(respath + year)
        print(f'{str(year)} pre:  {df.to_df().count()}')
        df.clean()
        print(f'{str(year)} post: {df.to_df().count()}')
        df.make_CountsOfNights()
        df.write_to_pkl(cleanpath
                        + 'CountsOfNights/'
                        + year[:-4] 
                        + '.pkl')
        print(f'Wrote {str(year[:-4])}')

    '''
    '''
    for year in list_res:
        df = Data(respath + year)
        df.clean()
        df.make_SumOfCategories()
        df.write_to_pkl(cleanpath
                        + 'SumOfCategories/'
                        + year[:-4] 
                        + '.pkl')
        print(f'Wrote {str(year[:-4])}')
    '''
    
    for year in list_res:
        df = Data(respath + year)
        df.clean()
        df.make_DistanceByWeekend()
        df.write_to_pkl(cleanpath
                        + 'DistanceByWeekend/'
                        + year[:-4] 
                        + 'NoAK.pkl')
        print(f'Wrote {str(year[:-4])}')

    for year in list_res:
        df = Data(respath + year)
        df.clean()
        df.make_DistanceByLonger()
        df.write_to_pkl(cleanpath
                        + 'DistanceByLonger/'
                        + year[:-4] 
                        + 'NoAK.pkl')
        print(f'Wrote {str(year[:-4])}')
    

    '''
    #lst = [data2006.df, data2007.df]
    #data0607 = combine(*lst)
    #print(f'Post combi: {data0607.count()}')
    '''