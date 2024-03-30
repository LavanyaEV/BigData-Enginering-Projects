### Introduction
- This project is related to ECOM store Analysis. Data can come from web/mobile applications and will be real time. Suppose we are mainly getting 2 entities orders and payment data. So downstream system should be denormalized and should support real-time streaming. So we will use Cassandra (NoSQL) for faster read and writes.
- Lets see what we are actually going to do. For each order that is generated, we will be simply ingesting /inserting this order data into target (Cassandra) in real time basis. In target, the table will be denormalized, i.e, one table will contain both order and payment details. Payment data will be generated for each order. Each payment_id should be related to an order_id.
- One thing to note is payment will only happen if an order is placed. So we will first join it with order table and if order_id is available for that payment, we will update that record in target. It can happen that there is no order_id for that particular payment. It can be because, payment data came before the order data as there was some delay/ technical issue from the source side. So we will keep all these unmatched data inside DLQ table (for unmatched records). Then once order data is available, we will have to write a separate application which will process the payment data in DLQ and join it with order data to update the target table. This can be scheduled batch-wise.

### Pre-Requisites
- GCP Free-tier account
- GCP CLI Installed (to execute gcloud commands)
- Docker
- Basic to Medium Python Knowledge
- ETL knowledge

### Tech Stacks Used
- GCP Pub-Sub
- Docker (for Cassandra)
- GCP IAM
- Python

### Architecture
![image](https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/11e550b3-ffb8-403e-8207-e17d03393c53)
We will have Python producer code producing Order and Payment data. Then we have a service in GCP called GCP Pub-Sub. It is similar to Kafka. Inside this, there will be 3 topics: Orders, Payments and DLQ_Payments. Then there will be Order consumer which will simply ingest the data to Cassandra. Payment consumer will ingest the valid data into Cassandra and unmatched data to DLQ_payment table. Cassandra will be hosted in Docker. 


