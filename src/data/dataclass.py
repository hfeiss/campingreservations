import pyspark as ps
from pyspark.sql.types import FloatType
from pyspark.sql.functions import udf, stddev, substring
from distance import get_lat, get_lng, get_dst

# Start a spark session
conf = ps.SparkConf()
conf.set('spark.cores.max', '6')
conf.set('spark.executor.memory', '10g')
conf.set('spark.executor.cores', '6')
conf.set('spark.driver.memory','10g')
conf.set('spark.sql.shuffle.partitions', '100')
spark = (ps.sql.SparkSession.builder 
        .master("local[*]") 
        .appName("Capstone I")
        .config(conf=conf)
        .getOrCreate()
        )
sc = spark.sparkContext

class Data(object):
    """
    Input
    File name / path to .csv (string)
    
    Init
    Creates a spark dataframe from the csv

    Possible Actions
    Select wanted columns
    Clean data
    Add wanted columns
    Write spark df to .csv
    """

    def __init__(self, filename):
        self.filename = filename
        self.raw = spark.read.csv(filename,
                                    header=True,
                                    inferSchema=True)
        self.raw.createOrReplaceTempView('temp')
        self.df = self.to_df()

    def clean(self):
        self.select_columns()
        self.remove_data_nulls()
        #self.remove_category_nulls()
        self.make_LengthOfStay()
        self.make_CustomerLatitude()
        self.make_CustomerLongitude()
        self.make_DistanceTraveled()
        self.cleaned = self.df

    def to_df(self):
        # Create & return a spark.df from the temp
        # For using spark methods on data objects
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
                        STRING(FacilityZIP),
                        FacilityLongitude,
                        FacilityLatitude,
                        STRING(CustomerZIP),
                        CustomerState,
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
            [   'OrderNumber',
                'FacilityID', 
                'FacilityLongitude',
                'FacilityLatitude',
                'CustomerZIP',
                'CustomerState',
                'StartDate',
                'EndDate'
            ])
        result.createOrReplaceTempView('temp')
        self.df = self.to_df()

    def remove_category_nulls(self):
        result = self.df.dropna(how = 'all', subset=
            [   'Tent',
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
        get_lat_udf = udf(get_lat, FloatType())
        result = self.df.withColumn('CustomerLatitude',
                    get_lat_udf(self.df['CustomerZIP']))
        result.createOrReplaceTempView('temp')
        self.df = self.to_df()

    def make_CustomerLongitude(self):
        get_lng_udf = udf(get_lng, FloatType())
        result = self.df.withColumn('CustomerLongitude',
                    get_lng_udf(self.df['CustomerZIP']))
        result.createOrReplaceTempView('temp')
        self.df = self.to_df()

    def make_DistanceTraveled(self):
        get_dst_udf = udf(get_dst, FloatType())
        result = self.df.withColumn('DistanceTraveled',
                    get_dst_udf(self.df['FacilityLatitude'],
                                self.df['FacilityLongitude'],
                                self.df['CustomerLatitude'],
                                self.df['CustomerLongitude']))
        result.createOrReplaceTempView('temp')
        self.df = self.to_df()

    def make_LengthOfStay(self):
        result = self.df.selectExpr('*',
                            ''' 
                            DATEDIFF(EndDate, StartDate) 
                            as LengthOfStay
                            ''')
        result.createOrReplaceTempView('temp')
        result = spark.sql('''
                    SELECT
                        *
                    FROM
                        temp
                    WHERE
                        LengthOfStay < 17
                    ''')
        result.createOrReplaceTempView('temp')
        self.df = self.to_df()

    def write_to_pkl(self, path):
        '''
        Input
        spark df
        name (string)

        Output
        csv
        '''
        self.df.select('*').toPandas().to_pickle(path)

    def make_DistanceByWeekend(self):
        result = spark.sql('''
                    SELECT
                        *
                    FROM
                        temp
                    WHERE
                        LengthOfStay < 3 AND
                        CustomerState != 'AK'
                    ''')
        result.createOrReplaceTempView('temp')
        result = spark.sql('''
                    SELECT
                        AVG(DistanceTraveled),
                        MAX(DistanceTraveled),
                        MIN(DistanceTraveled),
                        STDDEV(DistanceTraveled) AS StddevDist
                    FROM
                        temp
                    ''')
        result.createOrReplaceTempView('temp')
        self.df = self.to_df()

    def make_DistanceByLonger(self):
        result = spark.sql('''
                    SELECT
                        *
                    FROM
                        temp
                    WHERE
                        LengthOfStay > 2 AND
                        CustomerState != 'AK'

                    ''')
        result.createOrReplaceTempView('temp')
        result = spark.sql('''
                    SELECT
                        AVG(DistanceTraveled),
                        MAX(DistanceTraveled),
                        MIN(DistanceTraveled),
                        STDDEV(DistanceTraveled) AS StddevDist
                    FROM
                        temp
                    ''')
        result.createOrReplaceTempView('temp')
        self.df = self.to_df()

    def make_CountsOfNights(self):
        result = spark.sql('''
                    SELECT
                        LengthOfStay,
                        COUNT(LengthOfStay)
                    FROM
                        temp
                    GROUP BY
                        LengthOfStay
                    ORDER BY
                        LengthOfStay
                    ''')
        result.createOrReplaceTempView('temp')
        self.df = self.to_df()
    
    def make_SumOfCategories(self):
        result = spark.sql('''
                    SELECT
                        SUM(Tent) AS Tent,
                        SUM(Popup) AS Popup,
                        SUM(Trailer) AS Trailer,
                        SUM(RVMotorhome) AS RVMotorhome,
                        SUM(Boat) AS Boat,
                        SUM(Car) AS Car,
                        SUM(FifthWheel) AS FifthWheel,
                        SUM(Van) AS Van,
                        SUM(CanoeKayak) AS CanoeKayak,
                        SUM(BoatTrailer) AS BoatTrailer,
                        SUM(PowerBoat) AS PowerBoat,
                        SUM(PickupCamper) AS PickupCamper,
                        SUM(LargeTentOver9x12) AS LargeTentOver9x12,
                        SUM(SmallTent) AS SmallTent
                    FROM
                        temp
                        ''')
        result.createOrReplaceTempView('temp')
        self.df = self.to_df()            

    def make_DistanceByCustomerZIP(self):
        result = spark.sql('''
                    SELECT
                        SUBSTRING('CustomerZIP', 1, 5)
                        AS CustomerZIP,
                        DistanceTraveled
                    FROM
                        temp
                    ''')
        result.makeOrReplaceTempView('temp')
        result = spark.sql('''
                    SELECT
                        CustomerZIP,
                        AVG(DistanceTraveled)
                    FROM
                        temp
                    GROUP BY
                        CustomerZIP
                    ''')
        result.makeOrReplaceTempView('temp')
        self.df = self.to_df()

    def make_DistanceByFacilityZIP(self):
        result = spark.sql('''
                    SELECT
                        SUBSTRING('FacilityZIP', 1, 5)
                        AS CustomerZIP,
                        DistanceTraveled
                    FROM
                        temp
                    ''')
        result.makeOrReplaceTempView('temp')
        result = spark.sql('''
                    SELECT
                        CustomerZIP,
                        AVG(DistanceTraveled)
                    FROM
                        temp
                    GROUP BY
                        CustomerZIP
                    ''')
        result.makeOrReplaceTempView('temp')
        self.df = self.to_df()