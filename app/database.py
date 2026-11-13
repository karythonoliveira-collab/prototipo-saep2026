from pathlib import Path
import sqlite3

DB_PATH = Path(__file__).resolve().parent.parent / 'banco.db'
SCHEMA_PATH = Path(__file__).resolve().parent.parent / 'bd.sql'

def conectar():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foregin_keys = ON')
    return conn

def preparar_banco():
    with conectar() as conn:
        conn.executescript(SCHEMA_PATH.read_text(encoding='utf-8'))
