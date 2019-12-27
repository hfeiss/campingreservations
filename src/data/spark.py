import pyspark as ps
from pyspark.sql.types import *
import datetime
import os
from zipcoords import zipcode_to_coords

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

# Function for mapping coordinants if none exist.


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
        self.temp_df = self.raw.createOrReplaceTempView('temp')
    
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
        self.temp_df = self.selected_columns.createOrReplaceTempView('temp')
    
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
        self.temp_df = self.coords.createOrReplaceTempView('temp')

    def make_customer_coords(self):
        # withColumn...
        self.temp_df = self.coords.createOrReplaceTempView('temp')

    def remove_nulls(self):
        pass

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

if __name__ == '__main__':
    data = Data(rawpath + 'reservations_rec_gov/2008.csv')
    data.select_columns()
    print(data.to_df().count())
    data.make_cleaned_coords()
    print(data.to_df().count())
    #data.make_cleaned_coords()
    #data.selected_columns()
    #data.select_columns()
    data.to_df().show(10)
    #data = data.make_cleaned_coords
    #data.make_cleaned_coords()
    #data.to_df().show(10)
    #print(data.count())
    #data.to_df().printSchema()
    