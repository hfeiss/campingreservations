import pyspark as ps
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
sc.setLogLevel('ERROR')


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
        self.raw = spark.read.csv(filename, header=True)
        self.temp = self.raw.createOrReplaceTempView('temp')
    
    def select_columns(self):
        self.columns = spark.sql(f'''
                                    SELECT
                                        OrderNumber,
                                        UseType,
                                        FacilityID,
                                        FacilityZIP,
                                        FacilityLongitude,
                                        FacilityLatitude,
                                        CustomerZIP,
                                        TotalPaid,
                                        StartDate,
                                        EndDate,
                                        NumberOfPeople,
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
        return self.columns
    
    def make_cleaned_coords(self):
        # if we don't have coords and do have zip
        pass

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

if __name__ == '__main__':
    #data = Data(rawpath + 'reservations_rec_gov/2006.csv').select_columns()
    #data.printSchema()