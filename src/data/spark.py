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
        self.selected_columns = spark.sql('''
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
                                        Tent,
                                        Popup,
                                        Trailer,
                                        RVMotorhome,
                                        Boat,
                                        Car,
                                        FifthWheel,
                                        Van,
                                        CanoeKayak,
                                        BoatTrailer,
                                        PowerBoat,
                                        PickupCamper,
                                        LargeTentOver9x12,
                                        SmallTent
                                    FROM
                                        temp
                                    ''')
        self.selected_columns.createOrReplaceTempView('temp')
        self.current = self.to_df()

    
    # Not used.
    # Found 0 instances where ZIP but not coords
    def check_facility_zips(self):
        self.coords = spark.sql('''
                                SELECT
                                    OrderNumber
                                FROM
                                    temp
                                WHERE
                                    FacilityZIP IS NOT NULL AND
                                    FacilityLongitude is NULL
                                ''')
        self.coords.createOrReplaceTempView('temp')
        self.current = self.to_df()

    def make_customer_coords(self):
        # need to deal with long zipcodes...
        result = self.current.withColumn('CustomerLatitude', get_lat_udf(self.current['CustomerZIP']))\
                    .withColumn('CustomerLongitude', get_lng_udf(self.current['CustomerZIP']))
        result.createOrReplaceTempView('temp')
        self.current = result

    def remove_nulls(self):
        self.current.dropna(how = 'any', subset = ['OrderNumber', 'FacilityID', 
            'FacilityLongitude', 'FacilityLatitude', 'CustomerZIP', 'StartDate',
            'EndDate'])

    def make_datetimes(self):
        pass
    
    def make_ids_integers(self):
        pass

    def combine(self):
        pass

    def clean(self):
        pass        

    def write_to_csv(self):
        pass

if __name__ == '__main__':
    data = Data(rawpath + 'reservations_rec_gov/2006.csv')
    data.select_columns()
    print(data.to_df().count())
    data.make_customer_coords()
    #data.selected_columns()
    #data.select_columns()
    data.current.show(10)
    #data = data.make_cleaned_coords
    #data.make_cleaned_coords()
    #data.to_df().show(10)
    #print(data.count())
    #data.to_df().printSchema()
    