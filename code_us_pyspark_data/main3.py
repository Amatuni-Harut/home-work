from pyspark.sql import SparkSession
from pyspark.sql import functions as F
spark=SparkSession.builder \
    .appName("csv_File") \
    .master("local[*]") \
    .getOrCreate()

df=spark.read.csv("data.csv",
                  header=True,
                  inferSchema=True)
"""
print(50*"=")
df.show(5)
print(50*"=")
df.describe().show()
print(50*"=")
df.printSchema()
print(50*"=")
print(df.columns)
print(50*"=")
df.select("host_id","host_name").show(5)
print(50*"=")
df.filter(df.price>300).show()
print(50*"=")


print(f"row: {df.count()}")
print(50*"=")
print(f"col: {len(df.columns)}")
print(50*"=")
df.groupBy("neighbourhood_group").count().show()
"""
print(200*"=")
df.select("room_type").distinct().show()
spark.stop()
