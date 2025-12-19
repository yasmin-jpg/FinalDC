import json
import pandas as pd
from kafka import KafkaConsumer

from db_utils import create_events_table, insert_event


def clean_and_store():
    consumer = KafkaConsumer(
        "raw_electricity",
        bootstrap_servers="localhost:9092",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset="earliest",
        enable_auto_commit=True
    )

    create_events_table()
    count = 0

    for message in consumer:
        item = message.value

        try:
            period = pd.to_datetime(item["period"]).isoformat()
            value = float(item["value"])

            if value < 0:
                continue

            insert_event(
                period=period,
                respondent=item.get("respondent"),
                fueltype=item.get("fueltype"),
                value=value
            )

            count += 1
            if count >= 500:
                break

        except Exception as e:
            print("Skip record:", e)
            continue


if __name__ == "__main__":
    clean_and_store()