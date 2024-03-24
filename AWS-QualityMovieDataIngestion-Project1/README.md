### Introduction
This project is regarding Quality Movie Data Ingestion in AWS. Dataset can be found in the project folder. This is going to be batch processing where we will get data everyday from IMDB and will process it and put in redshift. Since we are ingesting quality movie data, we should have some data quality checks. Eg: rating>8, some columns should not be null etc. We will consume data from S3, then evaluate Data Quality checks. Based on its result, we will ingest succesful data to Redshift table and failed data to some S3 location for analysis.

### Pre-Requisites
- AWS Free-tier account
- Basic Understanding of various AWS services
- Basic Python Knowledge
- ETL knowledge

### AWS Services Used
- S3
- Redshift
- Glue Crawlers, ETL jobs, DataBases
- EventBridge
- SNS

### Architecture Flow
 <img width="493" alt="Architecture" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/7aa2c298-4d7b-402e-a54e-2a24d1221065">

- Consume data from S3
- Consume data from S3
- Evaluate Data Quality checks 
- Either proceed or terminate Glue job, if data quality rule fails. If it is failed, log it into EventBridge and get notified on email (SNS)
- Ingest succesful records into Redshift and failed records into S3, which can be analyzed later.

### Step-By-Step Explanation
- First, upload the imbd_movies_rating.csv file to S3 bucket.
<img width="300" alt="S3" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/326d3e5c-6511-4741-a4c9-cf2bfe6d8261">

- Now create a redshift cluster by giving username and password. Inside that create target table in Redshift using script given inside this project folder.
<img width="400" alt="redshift" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/b4ba2209-aa79-46df-8d28-8c6cdc5317e1">
<img width="400" alt="table" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/f66d3428-36dc-4d71-8196-7a56b2a1d1b3">

- Now we have to crawl both movies_csv file and this redshift target table in order to get the metadata(schema and datatypes) which will be stored in Glue Database (create a database in Glue in order to store these metadata), so that we can directly make use of Glue Catalog. Below is the S3 crawler with source given as the s3 movies.csv file in our s3 bucket. Also attach the IAM role with all necessary policies as given below.Run the crawler, the metadata will get stored inside the Database.
<img width="400" alt="database" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/34ae68ed-44f7-4537-bafc-16e0741afd45">
<img width="400" alt="S3crawler" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/69c65090-208d-4a19-897f-925430990bac">
<img width="400" alt="iam" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/a3930cb5-d321-4ab8-b8cf-026976f1499b">

- In order to create crawler for Redshift (so that crawler can crawl target table in redshift), we require a jdbc connection. So go to Connection in Glue and click create connection. Give the source as Redshift and then select the cluster we created, give its username and password and then create the connection. Now go to crawlers, and then create a crawler for Redshift target table with source as JDBC and target as the Database(that we created under Glue Database to store metadata that is crawled by crawled) in order to store the metadata.
<img width="400" alt="connection" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/e055ea73-422e-415f-854a-f13c10c50b71">
<img width="400" alt="redshiftcrawler" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/9ebd2013-22da-411b-a2c5-8669dba60a54">

- Now run the crawler, you will get below error. But u can see that we have attached all the necessary policies with IAM role. So the reason why its happening is, redshift has to maintain some internal things etc in S3. So S3 is not under the same VPC, that’s why its giving error. So we have to create an endpoint for our S3 in the same region of our Redshift 

 



