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

    rows = []
    max_records = 500

    
    for message in consumer:
        rows.append(message.value)

        if len(rows) >= max_records:
            break

    
    df = pd.DataFrame(rows)

    
    df["period"] = pd.to_datetime(df["period"], errors="coerce")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    
    df = df.dropna(subset=["period", "value"])
    df = df[df["value"] >= 0]

    
    for _, row in df.iterrows():
        insert_event(
            period=row["period"].isoformat(),
            respondent=row.get("respondent"),
            fueltype=row.get("fueltype"),
            value=float(row["value"])
        )


if __name__ == "__main__":
    clean_and_store()
