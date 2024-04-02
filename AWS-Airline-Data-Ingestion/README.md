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
<img width="410" alt="iam" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/f1c4056a-e1ad-45df-bc6f-2e45fb8ac540">














