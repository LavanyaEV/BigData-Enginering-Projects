import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from awsglue import DynamicFrame
import re

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Script generated for node Flights Data
FlightsData_node1711872424681 = glueContext.create_dynamic_frame.from_catalog(database="airline-data-catalog", table_name="airline_dataset_gds", transformation_ctx="FlightsData_node1711872424681")

# Script generated for node Airports Data
AirportsData_node1711872867918 = glueContext.create_dynamic_frame.from_catalog(database="airline-data-catalog", table_name="dev_airlines_airports_dim",  redshift_tmp_dir="s3://temp-s3-data-dir/airport_dim/",transformation_ctx="AirportsData_node1711872867918")

# Script generated for node Filter
Filter_node1711872657612 = Filter.apply(frame=FlightsData_node1711872424681, f=lambda row: (row["depdelay"] > 60), transformation_ctx="Filter_node1711872657612")

# Script generated for node Join for Departure
Filter_node1711872657612DF = Filter_node1711872657612.toDF()
AirportsData_node1711872867918DF = AirportsData_node1711872867918.toDF()
JoinforDeparture_node1711873450868 = DynamicFrame.fromDF(Filter_node1711872657612DF.join(AirportsData_node1711872867918DF, (Filter_node1711872657612DF['originairportid'] == AirportsData_node1711872867918DF['airport_id']), "left"), glueContext, "JoinforDeparture_node1711873450868")

# Script generated for node Select Fields
SelectFields_node1711877918498 = SelectFields.apply(frame=JoinforDeparture_node1711873450868, paths=["carrier", "destairportid", "depdelay", "arrdelay", "city", "name", "state"], transformation_ctx="SelectFields_node1711877918498")

# Script generated for node Change Schema
ChangeSchema_node1711878101634 = ApplyMapping.apply(frame=SelectFields_node1711877918498, mappings=[("carrier", "string", "carrier", "string"), ("destairportid", "long", "destairportid", "long"), ("depdelay", "long", "depdelay", "long"), ("arrdelay", "long", "arrdelay", "long"), ("city", "string", "dep_city", "string"), ("name", "string", "dep_airport", "string"), ("state", "string", "dep_state", "string")], transformation_ctx="ChangeSchema_node1711878101634")

# Script generated for node Join for Arrival
ChangeSchema_node1711878101634DF = ChangeSchema_node1711878101634.toDF()
AirportsData_node1711872867918DF = AirportsData_node1711872867918.toDF()
JoinforArrival_node1711878258641 = DynamicFrame.fromDF(ChangeSchema_node1711878101634DF.join(AirportsData_node1711872867918DF, (ChangeSchema_node1711878101634DF['destairportid'] == AirportsData_node1711872867918DF['airport_id']), "left"), glueContext, "JoinforArrival_node1711878258641")

# Script generated for node Select Fields
SelectFields_node1711878389836 = SelectFields.apply(frame=JoinforArrival_node1711878258641, paths=["carrier", "depdelay", "arrdelay", "dep_city", "dep_airport", "dep_state", "airport_id", "city", "name", "state"], transformation_ctx="SelectFields_node1711878389836")

# Script generated for node Change Schema
ChangeSchema_node1711878467499 = ApplyMapping.apply(frame=SelectFields_node1711878389836, mappings=[("carrier", "string", "carrier", "varchar"), ("depdelay", "long", "dep_delay", "bigint"), ("arrdelay", "long", "arr_delay", "bigint"), ("dep_city", "string", "dep_city", "varchar"), ("dep_airport", "string", "dep_airport", "varchar"), ("dep_state", "string", "dep_state", "varchar"), ("city", "string", "arr_city", "varchar"), ("name", "string", "arr_airport", "varchar"), ("state", "string", "arr_state", "varchar")], transformation_ctx="ChangeSchema_node1711878467499")

# Script generated for node Amazon Redshift
AmazonRedshift_node1711878686628 = glueContext.write_dynamic_frame.from_options(frame=ChangeSchema_node1711878467499, connection_type="redshift", connection_options={"redshiftTmpDir": "s3://aws-glue-assets-590184124963-us-east-2/temporary/", "useConnectionProperties": "true", "dbtable": "airlines.daily_flights_fact", "connectionName": "redshift-connection", "preactions": "CREATE TABLE IF NOT EXISTS airlines.daily_flights_fact (carrier VARCHAR, dep_delay VARCHAR, arr_delay VARCHAR, dep_city VARCHAR, dep_airport VARCHAR, dep_state VARCHAR, arr_city VARCHAR, arr_airport VARCHAR, arr_state VARCHAR);"}, transformation_ctx="AmazonRedshift_node1711878686628")

job.commit()