import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "saep_db.sqlite")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='Usuario'")
        table_exists = cur.fetchone()[0] > 0
        if not table_exists:
            sql_file = os.path.join(os.path.dirname(__file__), "bancoPOP.sql")
            if os.path.exists(sql_file):
                with open(sql_file, "r", encoding="utf-8") as f:
                    sql_script = f.read()
                conn.executescript(sql_script)
                conn.commit()
    finally:
        conn.close()
