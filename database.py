import sqlite3
from datetime import datetime, date, timedelta
from pathlib import Path

DB_PATH = Path(__file__).parent / "electricity.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            record_date TEXT UNIQUE,
            surplus REAL,
            amount REAL,
            room_name TEXT,
            daily_usage REAL,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_record(surplus, amount, room_name, daily_usage=None):
    today = date.today().isoformat()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT surplus FROM records WHERE record_date = ?", (today,))
    existing = cursor.fetchone()
    
    if existing:
        cursor.execute("""
            UPDATE records 
            SET surplus=?, amount=?, room_name=?, daily_usage=?, created_at=?
            WHERE record_date=?
        """, (surplus, amount, room_name, daily_usage, now, today))
    else:
        cursor.execute("""
            INSERT INTO records (record_date, surplus, amount, room_name, daily_usage, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (today, surplus, amount, room_name, daily_usage, now))
    
    conn.commit()
    conn.close()

def get_yesterday_surplus():
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT surplus FROM records WHERE record_date = ?", (yesterday,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def get_history(limit=30):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT record_date, surplus, amount, daily_usage, room_name
        FROM records
        ORDER BY record_date DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows
