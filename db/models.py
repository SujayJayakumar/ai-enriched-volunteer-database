import sqlite3
from datetime import datetime

DB_PATH = "data/volunteer_data.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()

    with open("db/schema.sql", "r", encoding="utf-8") as f:
        cursor.executescript(f.read())

    conn.commit()
    conn.close()


def insert_member(clean_row):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO members (
            name,
            city,
            join_date,
            last_active,
            ingestion_ts,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            clean_row["name"],
            None,  # city unknown
            None,  # join_date unknown
            clean_row["last_active"],
            datetime.utcnow().isoformat(),
            "ingested"
        )
    )

    member_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return member_id
