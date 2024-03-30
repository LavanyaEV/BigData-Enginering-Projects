### Introduction
- This project is related to ECOM store Analysis. Data can come from web/mobile applications and will be real time. Suppose we are mainly getting 2 entities orders and payment data. So downstream system should be denormalized and should support real-time streaming. So we will use Cassandra (NoSQL) for faster read and writes.
- Lets see what we are actually going to do. For each order that is generated, we will be simply ingesting /inserting this order data into target (Cassandra) in real time basis. In target, the table will be denormalized, i.e, one table will contain both order and payment details. Payment data will be generated for each order. Each payment_id should be related to an order_id.
- One thing to note is payment will only happen if an order is placed. So we will first join it with order table and if order_id is available for that payment, we will update that record in target. It can happen that there is no order_id for that particular payment. It can be because, payment data came before the order data as there was some delay/ technical issue from the source side. So we will keep all these unmatched data inside DLQ table (for unmatched records). Then once order data is available, we will have to write a separate application which will process the payment data in DLQ and join it with order data to update the target table. This can be scheduled batch-wise.

### Pre-Requisites
- GCP Free-tier account
- GCP SDK Installed (to execute gcloud cli commands)
- Docker
- Basic to Medium Python Knowledge
- ETL knowledge

### Tech Stacks Used
- GCP Pub-Sub
- Docker (for Cassandra)
- GCP IAM
- Python

### Architecture
<img width="400" alt="Architecture" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/11e550b3-ffb8-403e-8207-e17d03393c53">

We will have Python producer code producing Order and Payment data. Then we have a service in GCP called GCP Pub-Sub. It is similar to Kafka. Inside this, there will be 3 topics: Orders, Payments and DLQ_Payments. Then there will be Order consumer which will simply ingest the data to Cassandra. Payment consumer will ingest the valid data into Cassandra and unmatched data to DLQ_payment table. Cassandra will be hosted in Docker. 

### Step-by-Step Explanation
- GCP SDK should be installed in order to execute GCP CLI commands. Open Pub/Sub service. Click on create topic. Give name, also click on Add default subscription. Here, Subscriber ID will be created for each topic and thiS ID will be used in our consumer code.
<img width="400" alt="pub-sub" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/9f1c2021-2a5f-4ece-a3d8-70e019c149f8">

- Now go to subscriptions and there u can see the subscription_id, topic name etc. You can also edit the retention policies. Similarly, create the 3 topics Orders, Payments, DLQ_Payments.
<img width="400" alt="topic" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/d8966db3-c7f2-4f71-a2a8-4bb0fa72771b">
<img width="400" alt="topic" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/6813f995-c799-403b-9b27-09e519e87a6b">

- Now we have to write the producer code, it will actually try to interact with these services. So first make sure you have installed GCP SDK in order to access Gcloud cli commands from your terminal.
Then you have to authenticate using below command.
<img width="450" alt="docker" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/1c26932f-ba88-489b-bdd1-2dc5f50515a5">

- This will open a new browser. There you have to select the same account which you created the gcp account, then enter credentials and you will get authenticated from this terminal. As soon as you authenticate, on the terminal it will display all the information, i.e, in which configuration file it has configured your credentials (the similar way of setting up AWS configure). This creates a json type of configuration file and that information will be displayed on the terminal itself, i.e, in which path it has actually configured. If we open that file, we can see this type of information. You can see the project_id, accesskey etc.
<img width="450" alt="docker" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/0f8c4eda-d67c-41e5-94a8-d1c8dd2c85aa">
<img width="400" alt="json" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/d1726441-660d-42ad-9c0b-dd7549954e85">

- After authenticating, it will create very basic and default level of credentials. But here, from the producer code, we want to connect to Pub-Sub service, then publish the data and consume it. So we need to provide those policies here, you need to create a role. So first you need to create a Service Account inside that gcp account, then assign the publisher- consumer role to that service account, and whatever credentials will get generated for this service account, we need to paste that details in the above config file.
- For creating this service account, go to IAM & Admin service. Go to service account. Provide a name. Attach 2 policies related to pub-sub as below, then keep other options default and click on done. Now click on service account created. There will be no keys. Click on 3 dots. Click on Manage Keys.
<img width="400" alt="iam" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/f2a64d75-617b-4f9d-8fa9-3f67e0d4fe77">
<img width="400" alt="iam" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/8ee9c38b-fccb-4ccb-b033-9122c09c5081">

- Then click on Create key. Give key type as json and it will get downloaded. Open that json file, you can exactly see content as above screenshot. Copy paste this json to the above configuration file that was already created while doing authentication.
<img width="400" alt="iam" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/1b84a970-d3a8-40b0-8968-03b406fd6d7f">

- Now we need to install 2 python packages. Since we will interact with GCP Pub-Sub, we have to install this package. Also data will be consumed by Cassandra, so you have to install Cassandra-driver also.
![image](https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/105789a2-a0aa-4c2f-8330-2d997cded21a)
- Now we will see how to set-up Cassandra cluster. Below is the command to initiate Cassandra cluster. We have docker compose file in our repo. Check in docker whether Cassandra cluster is initiated.
![image](https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/4eefdbb6-1399-4e0b-acd4-e17259338551)
<img width="400" alt="docker" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/acc1d0f5-c8d3-4283-8b83-00da6519e603">
<img width="400" alt="docker" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/216b75e6-2c50-4b64-948b-41c7200448c0">

- Once Cassandra container starts, open the terminal of docker container. Click on that container above. Go to terminal. Type cqlsh on terminal. cqlsh shell will be opened and now Cassandra related commands can be executed. The consumed data should be put into denormalized table in Cassandra. You can find cql command in the repo to create the target table in Cassandra.
<img width="400" alt="docker" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/dda10de8-42a3-4164-94c8-13e908a601d2">

- Now understand producercodes. Check order_producer code. We have imported the pubsub modules. Then given project_id, topic_name etc. then generate mock data. This will continuously generate data in each 1-2 second. Payment_producer code is also similar. There we are giving order_id from 1-501 (for order_producer code, we gave 1-80) in order to intentionally fail the records.
<img width="400" alt="orderproducer" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/99dc8400-c337-430d-aa60-658454820214">
<img width="400" alt="paymentproducer" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/3a45cc74-9c44-4aed-bb00-0bc512bc1db6">

- Next look at the order_consumer code. We are establishing connection with Cassandra cluster and doing simple insert of whatever data is produced (we kept payment related columns as null as payment data will come later). In payment_consumer  code, we will first do a lookup whether order_id is present or not. If its present, we will update the record. Otherwise, we will throw an error mssg and put it in DLQ_Payment topic.
<img width="400" alt="orderconsumer" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/6306cd6a-e06a-49ad-aa98-854a30e21874">
<img width="400" alt="paymentconsumer" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/98b75b00-546a-4558-b3a3-f1a6ea718e1d">

- Open 4 terminals. Now start both consumer code. It will be in wait state until we run producer code. Now run the order_producer code. It will start publishing. Order_consumer will start consuming the data.
<img width="450" alt="orderproducer" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/2de36bb9-b49f-4658-87fe-50daf380f471">
<img width="400" alt="orderproducer" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/4f2bacfa-6296-4114-8e23-c0110821c74e">

- Now start the payment_producer code. You can see payment_consumer code has started consuming the data. After order_id 80, it will publish data back to dlq_topic (as order_id is missing).
<img width="450" alt="paymentconsumer" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/bc718738-fb67-4076-9a76-ec69c8b5d811">
<img width="400" alt="paymentconsumer" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/a73f0764-a44f-40a4-9129-b94bf7174b86">

- Now check Cassandra target table data. You can see some payment columns are null. Its becoz join didn’t happen.
<img width="400" alt="cassandra" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/141e3933-a106-47a2-939a-d0fb8fcb5ef0">

- Now, go to dlq_payment_topic in pub/sub. Click on pull. You can see the messages been published there.
<img width="400" alt="dlq" src="https://github.com/LavanyaEV/BigData-Enginering-Projects/assets/48172931/e12246e0-2e76-42d9-9434-cbf58135bf0d">

Congrats!! You have completed one more project..




























