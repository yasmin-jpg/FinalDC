import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "data" / "app.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def create_events_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        period DATETIME,
        respondent TEXT,
        fueltype TEXT,
        value REAL
    )
    """)

    conn.commit()
    conn.close()

def insert_event(period, respondent, fueltype, value):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO events (period, respondent, fueltype, value)
    VALUES (?, ?, ?, ?)
    """, (period, respondent, fueltype, value))

    conn.commit()
    conn.close()
