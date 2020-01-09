# Goal
![Granite Butte Lookout, Helena National Forest](/images/README/lookout.jpg)


Established in 2003, recreation.gov manages over 3 million reservations every year. These reservations are for anything from permit lotteries to fire-tower rentals in US National Parks and US Forest Service lands.

Every reservation made from 2006 through 2018 is available for public download through their API: about 10 gigabytes of .csv!

This repository explores the the factors that dertermine how far one is willing to travel to a campground, and how long they stay once there.

# Rawdata
![](/images/README/ridb.png)

The reservation data is provided as a seperate .csv for every year. Each year has 57 columns, 22 of which are (mostly) one-hot encoded category types. This analysis included: 

> OrderNumber •
> UseType •
> FacilityID •
> FacilityZIP •
> FacilityLongitude •
> FacilityLatitude •
> CustomerZIP •
> TotalPaid •
> StartDate •
> EndDate •
> OrderDate •
> NumberOfPeople •
> Tent •
> Popup •
> Trailer •
> RVMotorhome •
> Boat •
> Car •
> FifthWheel •
> Van •
> CanoeKayak •
> BoatTrailer •
> PowerBoat •
> PickupCamper •
> LargeTentOver9x12 •
> SmallTent

In addition to the reservations, relational databases of campground information are also available for download.

# Exploratory Analysis

EDA reveals relatively messy data. Of the 29,055,989 reservations, 12 columns have data in less than 1% of the rows. 

Interestingly,  `Marinaboat` has only one non-null value in all of the years. Further, that one non-null is not boolean: `e6100000 010c5bb0...`, and it is doubtful that someone parked their boat 5 miles inland at [Haleakala National Park's sunrise hike:](https://www.recreation.gov/ticket/facility/253731)

![](/images/README/marinaboat.jpg)

Formatting within the columns is mostly consistent, but does requrie type casting, truncation, and removing impurities.

For most quereis, 35% of the data is removed for either formating or nulls or. For sorting by `FacilityZIP`, an unfortunate 60% is removed due to nulls.

# Methods

### Big Data
This project uses an Amazon Web Service's m5a.8xlarge EC2 instance. The instance builds and runs a docker pyspark container. The scripts issue SQL queries into a SparkContext and the results of the queries are saved as .pickels in `data/cleaned`. The clean .pkl files are moved into S3 storage, and then downloaded for analysis on a local machine.

### Further Cleaning
The cleaned data are less than 10mb size: perfect for local analysis. The .pkl files are read into a pandas DataFrame. States outside of the United States are removed, as are reservations with impossible durations due to date boundries at the begining of year's dates.

### Matplotlib

### Folium

# Conclusions

# Further Analysis
Combine all years into one. Get total info from them.

Set up true distributed computation
Analize all years together
Add autosave