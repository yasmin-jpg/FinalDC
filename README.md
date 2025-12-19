Final  Project
API → Kafka → SQLite → Airflow

Project Description
This project shows a simple data pipeline:
We take data from the public API
We send them to Kafka (raw data), Clean the data and save it to SQLite
Building daily analytics
We manage the entire process through Apache Airflow
The project is educational, designed to understand the basics of Data Engineering.

Architecture
API
 ↓
Kafka topic (raw_electricity)
 ↓
Job 2: data cleanup
↓
SQLite (events, daily_summary)
↓
Job 3: Analytics

Technologies used

Python 3
Apache Kafka
Apache Airflow 3.x
SQLite
pandas
requests
kafka-python
Project structure
FinalProjDC/
│
├── airflow/
│   └── dags/
│       ├── job1_ingestion_dag.py
│       ├── job2_clean_store_dag.py
│       └── job3_daily_summary_dag.py
│
├── src/
│   ├── job1_producer.py
│   ├── job2_cleaner.py
│   ├── job3_analytics.py
│   └── db_utils.py
│
├── data/
│   └── app.db
│
├── venv/
,── README.md

The data source (API)
Uses a public API for generating electricity.
The data is received in JSON format and contains:
period — date/hour
respondent — company
fueltype — fuel type
value — the volume of generation

Job 1 — Ingestion (API → Kafka)
File: src/job1_producer.py
DAG: job1_ingestion
What does:

Requests data from the API
Sends each record to Kafka topic raw_electricity
Data is not cleared (raw)
Kafka topic is created by the team:
kafka-topics --create \
  --topic raw_electricity \
  --bootstrap-server localhost:9092 \
  --partitions 1 \
  --replication-factor 1

Job 2 — Cleaning & Storage (Kafka → SQLite)
File: src/job2_cleaner.py
DAG: job2_clean_store
What does:

Reads data from Kafka
Deletes incorrect values
Converts data types
Saves it to the events table in SQLite
The database is created automatically in:
data/app.db
Table events:
period
respondent
fueltype
value

Job 3 — Analytics (SQLite → SQLite)
File: src/job3_analytics.py
DAG: job3_daily_summary
What does:

Reads data from events
Groups by date and fuel type
Counts:
the average value
of the maximum
amount
Saves the result to the daily_summary table
Airflow
The launch of Airflow
airflow standalone

Web interface
http://localhost:8080

Checking
the airflow dags list
Checking the status of tasks
airflow tasks state job1_ingestion run_producer <run_id>
Why is DAG 1 without Schedule
job1_ingestion is configured as continuous ingestion, so:
schedule=None
The DAG is triggered manually or by an external trigger
This corresponds to the task condition
How to understand that everything is working
There are messages in Kafka (kafka-console-consumer)

SQLite has entries:
SELECT COUNT(*) FROM events;
SELECT COUNT(*) FROM daily_summary;
In the Airflow DAG, both are visible even without import errors

Result
The project demonstrates:
API work, data streaming via Kafka, storage in SQLite
orchestration via Airflow