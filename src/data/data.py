import pyspark as ps
from pyspark.sql.types import *
from pyspark.sql.functions import *
import datetime
import os
from zipcoords import get_lat, get_lng

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

get_lat_udf = udf(get_lat, FloatType())
get_lng_udf = udf(get_lng, FloatType())
get_len_udf = udf()

class Data(object):
    """
    Input
    File name / path to .csv (string)

    Actions
    Creates a spark dataframe
    Selects wanted columns
    Performs tasks such as cleaning

    Output
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
        

    def combine(self):
        pass

    def write_to_csv(self):
        pass

if __name__ == '__main__':
    data = Data(rawpath + 'reservations_rec_gov/2006.csv')
    print(data.to_df().count())
    data.clean()
    print(data.to_df().count())
    data.to_df().show(10)
    data.to_df().printSchema()
    