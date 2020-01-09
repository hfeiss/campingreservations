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

In addition to the reservations, relational databases of campground information are also available for download. One can extract another 50 attributes for every `FacilityID`.

# Exploratory Analysis

EDA reveals relatively messy data. Of the 29,055,989 reservations, 12 columns have data in less than 1% of the rows. 

Interestingly,  `Marinaboat` has only one non-null value in all of the years. Further, that one non-null is not boolean: `e6100000 010c5bb0...`, and it is doubtful that someone parked their boat 5 miles inland at [Haleakala National Park's sunrise hike:](https://www.recreation.gov/ticket/facility/253731)

![](/images/README/marinaboat.jpg)

Formatting within the columns is mostly consistent, but does require type casting, truncation, and removing impurities.

For most quereis, 35% of the data is removed for either formating or nulls. For sorting by `FacilityZIP`, an unfortunate 60% is removed due to nulls, but atleast 1 million rows remain in each year's data.

# Conclusions

## Distance Traveled vs. Number of Nights

This analysis found no direct correlation between the average distance traveled<sup>[1](#myfootnote1)</sup> , and number of nights one stays at a facility. In almost every year, the standard deviation of the averages is greater than the mean itself.

This data is complicated by rservations made to/from Alaska and Hawaii. Computation time did not allow for excluding these states as outliers.

![](/images/HypothesisTest.png)

However, the statistal distribution of the *averages for each year* do appear to differ with a pseudo p value of = 0.016

These results are counterintuitive; it seems people travel longer the shorter the stay! Also, the distances for travel are improbable for a "weekend warior" trip. Fundamentally, the analysis is not accounting for how people actually travel. The basis for this analysis is one travels from the home address to the facility. In reality, reservations are likely linked together on road trips and vacations.

![](/images/TypeOverTime.png)

The large - and growing - proportion of resevations made for RV's and other motorized transport suppor this notion.

## Distance by Customer's State
![](/images/CustomerState.gif)

As does the fact that, on average, reservations made from the North East, Flordia (and Hawaii and Alaska), are for a distance of +1,000 miles.

## Distance by Destination's State
![](/images/FacilityState.gif)

Lastly, year after year, reservations are made from across the country to visit Alaska and the Grand Canyon.

![](/images/README/manko.jpg)


# Methods

### Big Data
This project uses an Amazon Web Service's m5a.8xlarge EC2 instance. The instance runs and starts a docker pyspark container. The scripts issue SQL queries into a SparkContext for cleaning. Additionally, ZIP codes are converted into latitueds and longitudes, and the distance between the customer's home and the facility is calculated. The average computation time is 45 minutes per year.

Lastly, the results are saved as .pickels in `data/cleaned`. The clean .pkl files are moved into AWS S3 storage, for backup / download.

### Further Cleaning
The cleaned data are less than 10mb size: perfect for local analysis. The .pkl files are read into pandas DataFrames. States outside of the United States are removed, as are reservations with impossible durations due to date boundries at the begining of year's dates.

### Matplotlib
First, a histogram of the duration of stays is created. This histogram is used to decide the two "Length Of Stay" bins: weekend trips and trips longer than two nights.

![](/images/HistogramOfNights.png)

One's intuition is likely correct here. Reservations are usually two nights: the length of a weekend. Counts rapidly decline until another steep drop between 7 and 8 nights: the length of a week. Finally, there's a small spike at 14 nights: the maximum length of stay at most facilties.

### Folium
Finally, folium is used to generate maps of the average distance between the `CustomerZIP` and the campground's location given either the `CustomerState` or the `FacilityState`. Selenium.webdriver is used to generate .png images from the interative maps, and PIL converts them into .gif seen above.


# Further Analysis
Combine all years into one. Get total info from them.

Set up true distributed computation
Analize all years together
Add autosave

ZIP codes

bins for distnace

# Footnotes
<a name="myfootnote1">1</a>: as calculated by the orthdromic distance between a reservation's `customerZIP` code to a facility's (`FacilityLatitude`, `FacilityLongitude`). As mentioned in the conclusions, this is likely an innacurate measurment of the distance *actually* traveled.