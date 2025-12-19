import sqlite3
import pandas as pd

def run_analytics():
    conn = sqlite3.connect("data/app.db")

    df = pd.read_sql("SELECT * FROM events", conn)
    df["date"] = pd.to_datetime(df["period"]).dt.date

    summary = (
        df.groupby(["date", "fueltype"])
        .agg(
            avg_value=("value", "mean"),
            max_value=("value", "max"),
            total_value=("value", "sum")
        )
        .reset_index()
    )

    summary.to_sql("daily_summary", conn, if_exists="replace", index=False)
    conn.close()

if __name__ == "__main__":
    run_analytics()