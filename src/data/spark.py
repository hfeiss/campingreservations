import pyspark as ps
from pyspark.sql.types import *
from pyspark.sql.functions import udf
import datetime
import os
from zipcoords import get_lat, get_lng

srcpath = os.path.split(os.path.abspath(''))[0]
rootpath = os.path.split(srcpath)[0]
datapath = os.path.join(rootpath, 'data/')
rawpath = os.path.join(datapath, 'raw/')

spark = (ps.sql.SparkSession.builder 
        .master("local") 
        .appName("Capstone I")
        .getOrCreate()
        )
sc = spark.sparkContext

get_lat_udf = udf(get_lat, FloatType())
get_lng_udf = udf(get_lng, FloatType())

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
        self.raw = spark.read.csv(filename, header=True, inferSchema=True)
        self.raw.createOrReplaceTempView('temp')
        self.current = self.to_df()

    # Use this to create & return a spark.df from the temp
    # For spark methods outside of this class
    def to_df(self):
        result = spark.sql('''
                        SELECT
                            *
                        FROM
                            temp
                        ''')        
        return result      

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
        self.current = self.to_df()


    def make_customer_coords(self):
        # need to deal with long zipcodes...
        result = self.current.withColumn('CustomerLatitude',
                        get_lat_udf(self.current['CustomerZIP']))\
                    .withColumn('CustomerLongitude',
                        get_lng_udf(self.current['CustomerZIP']))
        result.createOrReplaceTempView('temp')
        self.current = self.to_df

    def remove_nulls(self):
        result = self.current.dropna(how = 'any', subset = ['OrderNumber', 'FacilityID', 
            'FacilityLongitude', 'FacilityLatitude', 'CustomerZIP', 'StartDate',
            'EndDate'])
        result.createOrReplaceTempView('temp')
        self.current = self.to_df()

    def clean(self):
        self.select_columns()
        self.remove_nulls()
        self.make_customer_coords()        

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
    