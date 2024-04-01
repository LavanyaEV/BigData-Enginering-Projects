### Introduction
This is related to the data movement of CDC events related to Product Sales data, capturing it and having it in the Datalake (S3). On top of S3, we will be doing analysis of the data. This will be a near real-time processing. DynamoDB stream will publish CDC events. Kinesis stream will consume cdc events. Kinesis firehose will batch the data in near-real time and will dump it to s3 (batching is needed becoz it does not make sense to put each event row by row to s3, so it will create a small batch). Athena is used for Data Analysis. We will connect DynamoDb and Kinesis using eventbringde pipe. To produce data, we will use python code to generate mock data. DynamoDb is a NOSQL in AWS. 

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




