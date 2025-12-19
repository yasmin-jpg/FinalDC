#src/job1_producer.py

import json
import time
import requests
from kafka import KafkaProducer

time.sleep(20)  

API_URL = "https://api.eia.gov/v2/electricity/rto/fuel-type-data/data/"
API_KEY = "eR4JMWIkjBWzSGGQ2T43RITLnnSIAFzGnktqJGL2"

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def fetch_data():
    params = {
        "api_key": API_KEY,
        "frequency": "hourly",
        "data[0]": "value",
        "sort[0][column]": "period",
        "sort[0][direction]": "desc",
        "length": 100
    }
    response = requests.get(API_URL, params=params)
    response.raise_for_status()
    return response.json()["response"]["data"]

def run():
    while True:
        records = fetch_data()
        for record in records:
            producer.send("raw_electricity", record)
        producer.flush()
        time.sleep(300)  # 5 минут

if __name__ == "__main__":
    run()
