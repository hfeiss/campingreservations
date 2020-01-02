lst = ['HistoricalReservationID', 'OrderNumber', 'Agency', 'OrgID', 'CodeHierarchy', 'RegionCode', 'RegionDescription', 'ParentLocationID', 'ParentLocation', 'LegacyFacilityID', 'Park', 'SiteType', 'UseType', 'ProductID', 'EntityType', 'EntityID', 'FacilityID', 'FacilityZIP', 'FacilityState', 'FacilityLongitude', 'FacilityLatitude', 'CustomerZIP', 'CustomerState', 'CustomerCountry', 'Tax', 'UseFee', 'TranFee', 'AttrFee', 'TotalBeforeTax', 'TotalPaid', 'StartDate', 'EndDate', 'OrderDate', 'NumberOfPeople', 'Tent', 'Popup', 'Trailer', 'RVMotorhome', 'Boat', 'HorseTrailer', 'Car', 'FifthWheel', 'Van', 'CanoeKayak', 'BoatTrailer', 'Motorcycle', 'Truck', 'Bus', 'Bicycle', 'Snowmobile', 'OffRoadlAllTerrainVehicle', 'PowerBoat', 'PickupCamper', 'LargeTentOver9x12', 'SmallTent', 'Marinaboat', 'LatLongPoint']

for work in lst:
    print(work)

HistoricalReservationID
OrderNumber
Agency
OrgID
CodeHierarchy
RegionCode
RegionDescription
ParentLocationID
ParentLocation
LegacyFacilityID
Park
SiteType
UseType
ProductID
EntityType
EntityID
FacilityID
FacilityZIP
FacilityState
FacilityLongitude
FacilityLatitude
CustomerZIP
CustomerState
CustomerCountry
Tax
UseFee
TranFee
AttrFee
TotalBeforeTax
TotalPaid
StartDate
EndDate
OrderDate
NumberOfPeople
Tent
Popup
Trailer
RVMotorhome
Boat
HorseTrailer
Car
FifthWheel
Van
CanoeKayak
BoatTrailer
Motorcycle
Truck
Bus
Bicycle
Snowmobile
OffRoadlAllTerrainVehicle
PowerBoat
PickupCamper
LargeTentOver9x12
SmallTent
Marinaboat
LatLongPoint

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
OrderDate,
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

sch = StructType([StructField('OrderNumber', StringType(), True),
                    StructField('UseType', StringType(), True),
                    StructField('FacilityID', IntegerType(), True),
                    StructField('FacilityZIP', IntegerType(), True),
                    StructField('FacilityLongitude', FloatType(), True),
                    StructField('FacilityLatitude', FloatType(), True),
                    StructField('CustomerZIP', IntegerType(), True),
                    StructField('TotalPaid', FloatType(), True),
                    StructField('StartDate', DateType(), True),
                    StructField('EndDate', DateType(), True),
                    StructField('NumberOfPeople', IntegerType(), True),
                    StructField('Tent', BooleanType(), True),
                    StructField('Popup', BooleanType(), True),
                    StructField('Trailer', BooleanType(), True),
                    StructField('RVMotorhome', BooleanType(), True),
                    StructField('Boat', BooleanType(), True),
                    StructField('Car', BooleanType(), True),
                    StructField('FifthWheel', BooleanType(), True),
                    StructField('Van', BooleanType(), True),
                    StructField('CanoeKayak', BooleanType(), True),
                    StructField('BoatTrailer', BooleanType(), True),
                    StructField('PowerBoat', BooleanType(), True),
                    StructField('PickupCamper', BooleanType(), True),
                    StructField('LargeTentOver9x12', BooleanType(), True),
                    StructField('SmallTent', BooleanType(), True)])


    def make_LengthOfStay(self):
        result = self.current.withColumn('LengthOfStay',
                self.current['EndDate'] - self.current['StartDate'])
        result.createOrReplaceTempView('temp')
        self.current = self.to_df()