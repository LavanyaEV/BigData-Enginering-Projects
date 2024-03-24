![image](https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/823f2e75-36a5-49fd-8e2e-937f201011e8)### Introduction
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

- In order to create crawler for Redshift (so that crawler can crawl target table in redshift), we require a jdbc connection. So go to Connection in Glue and click create connection. Give the source as Redshift and then select the cluster we created, give its username and password and then create the connection. Now go to crawlers, and then create a crawler for Redshift target table with source as JDBC (give the database/schema/targettable we created in Redshift), also select the connection we created above and then give target as the Database(that we created under Glue Database to store metadata that is crawled by crawled) in order to store the metadata.
<img width="400" alt="connection" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/e055ea73-422e-415f-854a-f13c10c50b71">
<img width="400" alt="redshiftcrawler" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/9ebd2013-22da-411b-a2c5-8669dba60a54">

- Now run the crawler, you will get below error. But u can see that we have attached all the necessary policies with IAM role. So the reason why its happening is, redshift has to maintain some internal things etc in S3. So S3 is not under the same VPC, that’s why its giving error. So we have to create an endpoint for our S3 in the same region of our Redshift. 
<img width="400" alt="error" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/905b3aa6-c4c2-48f1-8783-27917cb5dfed">

- To change that, click on the VPC link of our redshift cluster (go to cluster and go to properties, there u can see the VPC). Click on endpoints. Click create endpoint. Provide a name-> in services, select S3 and select below gateway-> select vpc same as that of redshift. Select the routing table attcahed with that, and now click create endpoint. You can see the endpoint for s3 created. Also create a VPC nedpoint for glue in similar way.
  
![image](https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/4c66825e-b5c8-451f-9f1b-b9dbf7d392c8)
![image](https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/92e801b0-b09b-4f93-bce9-4feb65635df4)
![image](https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/d154bad8-cc99-4245-bcc1-1fb1f84437f5)
![image](https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/07b8e1c6-eb08-423c-bf74-1955996042d7)
![image](https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/5522c8d2-f54a-42d9-b970-b759f93d6b35)
![image](https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/587fb395-c40a-4fe3-88e5-b970a862fda4)
- Now run the  crawler again. It will be succesful this time. Once done, go to the databse in glue and check the table that is created with the metadata of redshift table.
<img width="400" alt="metadata" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/0b3e9e33-e637-4197-908a-57694104021d">

- Now we need to create Data Quality rules. Go to the metadata of S3 crawler we created (inside glue database). Go to Data Quality option. click on create rule-set. If you are creating it for the first time, you have to execute that in order to get the recommendations. It will recommend all the rules after scanning the data, add the required rules (you can give the imdb rating range from 8 to 10, to get the quality data) and click create. You can see all the rules being added as the below image. Then click on save ruleset.
<img width="400" alt="dataquality" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/588cd62c-d5cc-46c6-8dc3-c99101beb55a">
<img width="400" alt="dataquality" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/8a72c374-8d95-4f16-88df-93a846a21d0b">
<img width="400" alt="insertrules" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/35f35c24-4e7d-45ad-9a61-f84fbe229495">
<img width="400" alt="insertrules" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/0956265e-0edd-43eb-8759-a63fef52a01c">
<img width="400" alt="rules" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/deaf17ec-e93f-40a2-84a6-8791181e47a1">

- Now, in order to get the data quality score, click on Run option above that ruleset that we created now. Then give the run details, attach the iam role, then also specify the result location (here, its an S3 bucket. You can create an S3 bucket to store these results and provide its location). Then click on run. Once its succesful, you can see the score (here, 95%, 41/43 rules passed). You can go to S3 location we gave, download the results and check where Data quality check got failed.
<img width="400" alt="rulescore" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/ea0ea595-32b8-4ef0-a062-91f070d29a40">
<img width="400" alt="rulescore" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/911dd4ea-2d02-45cf-b7c2-ceb2f56676f4">
<img width="400" alt="s3dq" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/09e6ca80-ecfb-45ad-884f-48261a4e44c7">

- Now we can create the glue job. Go to glue and select visual ETL. First give source as S3 and select the metadata catalog we created for movies.csv data.
<img width="400" alt="s3" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/73b91b8d-cee0-4092-84f6-e9a06e2caa77">

- Add Data Quality Evaluation component. Copy paste the rules we create in the above step to this one and provide other configuartions as below. Here, we will continue the job even if Data Quality check fails. You can see that Data quality events are being sent to Eventbridge.
<img width="400" alt="dq" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/b5ddadd3-d7a8-48d0-9f96-b0d1a65db228">
<img width="400" alt="dqconfig" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/96281d6d-2780-4cb8-a624-6afebb31333a">

- You can see there are 2 flows, since we tick 2 things above, one is for Data Quality results and another is for Original data. Thats why 2 flows got created. Data Quality Result (ruleOutcome) is used to get the pass or fail status of configured rules. It has some additional columns to see the status. This gives the high level overview of the rules we applied and its status (failed/success). Original Data (rowLevelOutcome) means it contains the original incoming data with rowlevel outcomes, i.e, it will have additional columns which gives the status(failed/success) of each row after applying data quality rules.
<img width="400" alt="flow1" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/bd4f354f-1c85-46d9-9621-d2e6af8782e6">
<img width="400" alt="flow2" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/52263bc0-572d-44b4-a8d1-ac35abdb2e7d">

- RuleOutcome you can directly put into an S3 bucket and you can analyze it. (you can create an S3 bucket rule_outcome/). Now for RowlevelOutcome (original data), there will be 2 flows for success and failure. So add a conditional router. It will have 2 flows, output_group and default_group.
<img width="400" alt="ruleoutcome" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/cdf9e9b5-60b1-423e-901f-90f73926b474">
<img width="400" alt="conditionalroute" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/287ab066-bcb8-4ceb-ad31-fc73dd044e66">

- Output_group means it defines a set of conditions a record/row has to meet in order to be routed to the output_group. So here we will check for the failed records by giving the below condition. All the successful records will go to default_group
<img width="400" alt="outputgroup" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/15d5fe03-ef7c-40ae-a1ef-247cd9ff04db">

- Now, we can route the failed records in he output_group to S3 bucket (u can create an s3 bucket called bad_data/) in order to analyze the failed records. We can also create Athena table on top of it for further analysis.
<img width="400" alt="conditionalroute" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/be22261e-6bda-4aee-914e-82b2dfdabeb3">

- Now, put the succesful records of the default_group to Redshift table. Before that, apply change schema in order to give the same datatype to columns as that of RedShift table (otherwise it will append the datatype and create a new column, if its not same). Then provide the redshift table details and the metadata catalog we created for Redshift table
<img width="400" alt="schemachange" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/22bdddc1-8d18-4c21-8209-66e32e562c72">
<img width="400" alt="redshift" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/cc8f7863-b74e-4098-80b3-a72741a4e31d">

- Our glue job will look like this. Go to Job details, attach the IAM role. Give no of workers as 2. Also, give the job_name parameter.
<img width="430" alt="glue" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/e8a1c380-df87-4e8c-ae90-31805c9122d6">
<img width="400" alt="glue" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/8a845a9e-b66d-441c-b002-a64553764a5d">

- Now run the job. You can see that the job fails and gives below error. It is because, as seen above, all the Data Quality check events are sent to eventbridge. But the monitoring connection is breaking, so we need to create the VPC endpoint for monitoring, giving the same vpc, subnet, security group as that of Glue job.
<img width="400" alt="vpc" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/92336ea0-f046-48be-8f77-75edb2f36ec5">
<img width="400" alt="vpc" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/83b95143-242b-4e4b-9e6f-69951714a682">

- Click on VPC link of redshift cluster and click on create endpoint. Seach monitoring and add the interface. Select the same vpc, subnet and security group as that of Connection. Then click on create endpoint.
<img width="400" alt="vpc" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/4743d221-3e75-4224-8d42-8e10eadc9055">
<img width="400" alt="vpc" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/bfb35563-aee6-4988-a741-e99bd554c7c2">
<img width="400" alt="vpc" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/ceb3a892-6965-4ad0-b880-0df979f514f7">











  




  



















 

 



