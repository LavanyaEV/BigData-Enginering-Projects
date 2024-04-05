### Introduction
This project is related to Logistics Data Ingestion. Here, we will daily receive a .csv file having logistics data, which contains delivery_id, destination, delivery_status, vehicle type etc. We will use Hive as our Data warehousing service and source is Google cloud Bucket. Target table should be partitioned. Also, target table ingestion should start as soon as the file arrives. 

### Pre-Requisites
- GCP Free-tier account
- Airflow Knowledge
- Knowledge of Hive/Hadoop Commands
- Basic to Medium Python Knowledge

### Tech Stacks Used
- GCP Bucket
- Composer (Managed Airflow)
- DataProc Cluster
- Hive Commands
- Python

### Architecture
<img width="400" alt="Architecture" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/37b741d4-f14f-46a1-a563-541cde326e67">

- In GCP bucket, inside input_data/ folder, we will receive logistics_yyyy_mm_dd.csv file everyday.
- Then create a staging table inside Dtaproc cluster (Hive) which should be external. External table will always point to input_data/ folder. So if there is x.csv file, once its read and if y.csv file comes, it will again read those 2 files creating duplicates (as its pointing to folder, not file). So we should remove the processed file from the folder, ie, we will have one more bucket to put the archived files, once the file is processed and moved to respective partitioned table, we should move it to this archival folder.
- We can see all these steps are dependent on each other, so we will use Airflow.

### Step-by-Step Explanation
- Open GCP Bucket, create one bucket for input_data/ and also create one bucket for Archival of processed files.
<img width="400" alt="bucket" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/e26e1f7f-18c9-488e-93eb-ec5a9a55b105">
<img width="400" alt="bucket" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/346daba4-e8ad-4dbf-8b39-24d2ea8f001f">

- Now, create a DataProc cluster(managed Hadoop, hive, spark cluster) with 2 worker nodes.
<img width="400" alt="dataproc" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/60939dcc-cc32-4c58-b0b3-7528bb34c6f3">

- Now, lets understand the Airflow DAG script. Code is inside repo. Below sensor operator is used to sense any data that comes into input bucket. Then we assigned default arguments for our DAG. Then we created a DAG object where we are scheduling it everyday. Then we wrote first task to sense input data. We are giving bucket name and folder name. we gave mode as ‘poke’, it means kind of polling, i.e, its continuously checking whether data came or not. Poke_interval:30 means  every 30 sec, it will check for the new file. Timeout:300 (5 mins) means for 5 mins, it will continue cheking for file after every 30 sec. If no file is received, it will timeout. If file is received, it will go to other tasks.
<img width="400" alt="code" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/9c588c00-1174-4fd1-ab35-2183892d1120">

- Then we create a database inside hive, if not exists. Then create External staging table pointing to input-data/ folder.
<img width="400" alt="code" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/38db4803-f0c0-4cab-8557-975bdde0c4b9">
<img width="400" alt="code" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/7ae2cd5b-13e9-4ad9-8541-0292fed0038b">

- Then create Partitioned table with partition key as date. Then we have to load the data from staging table to our dynamic partitioned table based on date(partition key). Set below 2 dynamic properties as true.
<img width="400" alt="code" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/b1d13b98-b0e5-4d07-bab3-54c2b095b8b9">
<img width="400" alt="code" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/8a482afd-5a80-48c5-9f0b-396a97f0ead1">

- Then move the processed file into Archival folder using move command. Then write the dependency between all these steps.
<img width="400" alt="code" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/55921551-844e-4985-9dd4-1bcf96e2d38f">

- 











