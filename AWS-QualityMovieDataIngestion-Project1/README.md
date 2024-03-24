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
  ![image](https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/7d31e76b-8290-4cff-bf4e-a04839166f7b)
