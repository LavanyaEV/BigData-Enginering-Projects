### Introduction
This project is related to processing of Airline Data. On a daily basis, we will be getting 60-65 files from the client application to our S3 bucket. Data is mainly related to flight booking, cancellation, customer data, checkin-data etc. Then we have to process this based on some business logic to get maximum insights out of it and improve the operations of flights. 

### Pre-Requisites
- AWS Free-tier account
- Medium level understanding of various AWS services
- Basic to Medium Python Knowledge
- ETL knowledge

### AWS Services Used
- Redshift
- S3
- Step Function
- Glue Job
- Glue Crawlers
- EventBridge Rule
- CloudTrail

### Architecture Flow
<img width="400" alt="Architecture" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/e1ecdbd2-6602-4a8d-a79d-74993ebe22ce">

- Client application will be dumping data to S3 daily. Its format is like date=2024-03-31/flights.csv. This mainly contains 5-6 columns including flight_operator, destination, departure_delay, arrival_delay, airport_code etc. Sample file is in repo. This data is very important to improve the operations of the flight.
- Airport_code is the code of different airports. But for the end-users, we have to show code and name of the airport. So source team provide dimension file also, i.e, airports.csv. This can be considered as the master data.
- This whole process has to be made event-driven. As soon as the data comes in S3, crawler will crawl all the new partitions (delta-data). We only need newly ingested data, so will do Glue Job bookmarking. If crawler is successful, Glue Job will execute and join delta-data of flights and Master data of Airports. If crawler fails, it will go to wait condition till the crawler is successful (otherwise we wont get updated partitions). Then glue job will dump data to Redshift table.
- Now from S3, it cannot directly trigger crawler. So we will create Eventbridge Rule which will check the PUT object kind of pattern (i.e, file format received in S3) and this rule will actually trigger the crawler.
- Now here there are some complexities involved including checking the success/failure status of crawler, then checking whether glue job is success/failure. All these are handled by **Step-Function**. This service is mainly used to orchestrate the AWS services and to create dependency and work-flow management (similar to airflow).

### Step-By-Step Explanation

- First create an S3 bucket for Airline data and upload airports.csv file (dimension file) into it.
<img width="380" alt="s3" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/2edf8225-7a04-4cdc-a67d-21cd1b0f2834">

- Next create a Redshift Cluster, open the Query Editor and inside that, create a table for airports.csv. Load airports data from S3 to this table. U can find queries in this repo (in below query, give the IAM role ARN of your redshift cluster). We are doing this so that glue job can utilize this table’s catalog to perform join operations.
<img width="400" alt="redshift" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/84556016-8657-4421-b5b9-19b60c3235aa">
<img width="400" alt="redshift" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/f8cdfa49-c232-4ff4-a42f-de13454d07a8">

- Now we need to create crawler on top of this Redshift table. Before that, we need to create a Connection to Redshift table. Go to Create Connection in AWS Glue. Give source as Redshift, give username and password of our Redshift Cluster and click create.
<img width="400" alt="connection" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/118187ec-c884-4be3-9601-fb79df31fcdb">

- Also we need to create S3-vpc-endpoint (redshift has to maintain some internal things etc in S3, so it has to be under the same VPC, otherwise it will throw error). For this, click on VPC link of our Redshift cluster. Go to Endpoints, click create endpoint, in services select S3 and select below gateway, select vpc same as that of redshift. Select the routing table attached with it, and click create.
<img width="400" alt="vpc" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/92c64e66-9fb8-4acf-a36f-68079b0dcab3">

- To create crawler, go to AWS Glue, first create a Glue Database for airline_data. Then click create Crawler. Give source as JDBC, provide the Connection we create above. Give database/schema/airports_dim. Attach IAM role with below policies. Give destination as the Database we created above, click create.
<img width="400" alt="crawler" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/71b7b4fb-581b-4306-addf-9536d9dfa965">
<img width="400" alt="iam" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/8eabc333-c4c5-46dc-b710-90ce1c3c1913">

- Run the crawler, check the Database table, you can see the Metadata Catalog created for airport table as below.
<img width="410" alt="database" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/f1c4056a-e1ad-45df-bc6f-2e45fb8ac540">

- Next create the target fact table inside Redshift. This is for daily Flights data we receive, and dump it to target table after joining with the master table (airports). Query is in repo.
<img width="400" alt="redshift" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/2bd05af4-8e48-4037-a5c7-7b575731f07d">

- Now, create a crawler to crawl this target table also, so that its catalog can be used by Glue job while joining it with master data. Create crawler, give source as JDBC. Give database/schema/daily_flight_fact. Give destination as the database we create above, click create. Run the crawler, you can check the Database to see the metadata information as below.
<img width="400" alt="database" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/e6bef153-302b-4df9-a1d1-e616da0374a9">
<img width="400" alt="database" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/531a9cca-61e7-4795-bbbf-50a86efd98d3">

- We will receive the daily data of flight from the source in partitioned form, like date, inside that flights.csv. If we want to read this delta file inside Glue job, we need to create a crawler on top of it and in glue job we will enable job-bookmarking as well so that incremental data is being read.
- Create crawler in order to crawl the daily flight data coming in S3. In source, give the S3 location. Select Crawl new sub-folders only option. Exclude pattern *airports.csv (becoz this is a dimension table which is already loaded to redshift, we don’t have to crawl it again, for eg, if someone deletes it and upload it again).
<img width="400" alt="crawler" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/15ae5060-61c2-494d-899b-61e7fa60ff69">

- The other 2 crawlers that we created for Redshift tables (master data and target table) has to be run only once. Flight_data crawler has to be run as soon as files are uploaded into S3 so that all new partitions can be crawled. Just upload a flights.csv file so this crawler crawls it and we get the metadata. Run the crawler and check database for metadata. Once crawler is successful, delete this folder.
<img width="400" alt="crawler" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/b55197e4-1a67-4eb2-9e65-f9010359d1df">
<img width="400" alt="crawler" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/05a8ad96-42b4-4bdc-8d38-379f5ea5d6be">

- Now we can set up Glue Job. Give the source as AWS Data Catalog (provide daily_flights data crawler result table). We have to apply filter on depdelay (departure delay) column in order to get only records with depdelay>60.
<img width="400" alt="glue" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/39710247-3443-4e8b-ac20-69644bef3e8e">

- Give the filter condition.
<img width="400" alt="glue" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/216324e0-fbd4-40ea-acd7-47327454fb93">

- Now we need one more Data Catalog source to get the Airport_dimension data. Select the table airport_dim that we crawled before. Since this is a redshift table, it puts some information in S3 bucket. So create an s3 bucket for temporary staging and provide its location. Select the same IAM role as that of our Redshift cluster.
<img width="400" alt="glue" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/e63bad92-16f9-47a0-8679-26dd42c96461">
<img width="400" alt="glue" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/4e34b0b9-10fe-466c-b69e-dcb556977dc9">

- Join the filtered data and Airports_dim data for departure.
<img width="400" alt="glue" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/a6bb1c4f-cf26-4194-bd6f-dff6512a4bb6">

- Perform Select fields (in order to select required fields) and change schema.
<img width="400" alt="glue" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/e9cc78a1-249e-4253-87f9-9acc97103b6e">
<img width="400" alt="glue" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/be3c975b-2724-4097-a952-d02bf632a81e">

- Again join the Change schema data and Airports_dim data for Arrival.
<img width="400" alt="glue" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/3acfec08-f479-44ad-934c-12b758d1459d">

- Again do Select fields (in order to select required fields) and change schema.
<img width="400" alt="glue" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/23af61d9-dbca-48de-ad21-50e28f58c955">
<img width="400" alt="glue" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/e898bf80-b61e-4ffd-9346-337bb3760520">

- Now provide the destination as Redshift with target as the fact table we created.
<img width="400" alt="glue" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/f1da9b58-bcf1-47e6-a5d3-a88f61c19007">

- Enable Glue Job Bookmarking. Change worker nodes to 2 and in parameters give –JOB_NAME. Then save this job. Now if you run this job it will throw error. Its becoz, in above step, we created a directory in S3 bucket for Airport_dim table(since it’s a redshift table; for S3 table you don’t need this). But if you check the script code, this directory won't be there. So glue job will break. So we have to edit the script to add this s3 directory path. Also, if we edit the script, we wont be able to see the visual ETL again.
<img width="400" alt="glue" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/74283933-4a3e-4b4d-b638-52cfc0c8ea90">
<img width="450" alt="glue" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/849f6b97-2216-4074-be05-52a5f1a4a215">

- Now we need to Orchestrate all these services. For that open the Step Function. This is like a DAG. Every node in that DAG is representing the current state of workflow, that’s why its called state machine. It internally uses AWS SDK’S and API to interact with various services.


































