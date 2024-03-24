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
![image](https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/74378793-61e2-4bf5-a530-720c27c977b3)
