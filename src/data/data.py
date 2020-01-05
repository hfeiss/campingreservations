import pyspark as ps
from zipcoords import get_lat, get_lng
from functools import reduce
import os

# Create filepaths within df directory
srcpath = os.path.split(os.path.abspath(''))[0]
rootpath = os.path.split(srcpath)[0]
datapath = os.path.join(rootpath, 'data/')
rawpath = os.path.join(datapath, 'raw/')

# Start a spark session
spark = (ps.sql.SparkSession.builder 
        .master("local") 
        .appName("Capstone I")
        .getOrCreate()
        )
sc = spark.sparkContext
sc.setLogLevel('ERROR')

# Define UDFs for lat and long fromm zip codes
get_lat_udf = udf(get_lat, FloatType())
get_lng_udf = udf(get_lng, FloatType())

class Data(object):
    """
    Input
    File name / path to .csv (string)

    Actions
    Init creates a spark dataframe from csv
    Selects wanted columns
    Cleans data
    Adds wanted columns
    Writes a cleaned .csv
    """

    def __init__(self, filename):
        self.filename = filename
        self.raw = spark.read.csv(filename,
                                    header=True,
                                    inferSchema=True)
        self.raw.createOrReplaceTempView('temp')
        self.df = self.to_df()

    # Use this to create & return a spark.df from the temp
    # For spark methods outside of this class
    def to_df(self):
        return spark.sql('''
                        SELECT
                            *
                        FROM
                            temp
                        ''')    

    def select_columns(self):
        result = spark.sql('''
                    SELECT
                        STRING(OrderNumber),
                        STRING(UseType),
                        INT(FacilityID),
                        FacilityLongitude,
                        FacilityLatitude,
                        CustomerZIP,
                        TotalPaid,
                        StartDate,
                        EndDate,
                        INT(NumberOfPeople),
                        INT(Tent),
                        INT(Popup),
                        INT(Trailer),
                        INT(RVMotorhome),
                        INT(Boat),
                        INT(Car),
                        INT(FifthWheel),
                        INT(Van),
                        INT(CanoeKayak),
                        INT(BoatTrailer),
                        INT(PowerBoat),
                        INT(PickupCamper),
                        INT(LargeTentOver9x12),
                        INT(SmallTent)
                    FROM
                        temp
                    ''')
        result.createOrReplaceTempView('temp')
        self.df = self.to_df()

    def remove_data_nulls(self):
        result = self.df.dropna(how = 'any', subset = 
            [
                'OrderNumber',
                'FacilityID', 
                'FacilityLongitude',
                'FacilityLatitude',
                'CustomerZIP',
                'StartDate',
                'EndDate'
            ])
        result.createOrReplaceTempView('temp')
        self.df = self.to_df()

    def remove_category_nulls(self):
        result = self.df.dropna(how = 'all', subset=
            [
                'Tent',
                'Popup',
                'Trailer',
                'RVMotorhome',
                'Boat',
                'Car',
                'FifthWheel',
                'Van',
                'CanoeKayak',
                'BoatTrailer',
                'PowerBoat',
                'PickupCamper',
                'LargeTentOver9x12',
                'SmallTent'
            ])
        result.createOrReplaceTempView('temp')
        self.df = self.to_df()

    def make_CustomerLatitude(self):
        result = self.df.withColumn('CustomerLatitude',
                    get_lat_udf(self.df['CustomerZIP']))
        result.createOrReplaceTempView('temp')
        self.df = self.to_df()

    def make_CustomerLongitude(self):
        result = self.df.withColumn('CustomerLongitude',
                    get_lng_udf(self.df['CustomerZIP']))
        result.createOrReplaceTempView('temp')
        self.df = self.to_df()

    def make_LengthOfStay(self):
        result = self.df.selectExpr('*',
                            ''' 
                            DATEDIFF(EndDate, StartDate) 
                            as LengthOfStay
                            ''')
        result.createOrReplaceTempView('temp')
        self.df = self.to_df()

    def clean(self):
        self.select_columns()
        self.remove_data_nulls()
        self.remove_category_nulls()
        self.make_CustomerLatitude()
        self.make_CustomerLongitude()     
        self.make_LengthOfStay()        

    def write_to_csv(self, name):
        pass

def combine(*dfs):
    # combines all dataframes
    # returns new spark dataframe
    return reduce(ps.sql.DataFrame.union, dfs)

if __name__ == '__main__':
    data2006 = Data(rawpath + 'reservations_rec_gov/2006.csv')
    print(f'Pre  clean: {data2006.to_df().count()}')
    data2006.clean()
    print(f'Post clean: {data2006.to_df().count()}')
    
    data2007 = Data(rawpath + 'reservations_rec_gov/2007.csv')
    print(f'Pre  clean: {data2007.to_df().count()}')
    data2007.clean()
    print(f'Post clean: {data2007.to_df().count()}')

    data0607 = combine(data2006.df, data2007.df)
    print(f'Post combi: {data0607.count()}')
