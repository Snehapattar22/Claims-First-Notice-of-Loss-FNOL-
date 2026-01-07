import sqlite3

DB_NAME = "claims.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS claims (
        claim_id TEXT PRIMARY KEY,
        policy_number TEXT,
        incident_type TEXT,
        incident_date TEXT,
        location TEXT,
        description TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()
