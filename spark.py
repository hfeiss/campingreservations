import pyspark as ps
import matplotlib.pyplot as plt
import datetime

spark = (ps.sql.SparkSession.builder 
        .master("local") 
        .appName("Spark Case Study") 
        .getOrCreate()
        )
sc = spark.sparkContext
sc = sc.setLogLevel('ERROR')



df = spark.read.csv('reservations2018.csv')

df.show(5)
