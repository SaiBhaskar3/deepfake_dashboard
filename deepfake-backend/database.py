# database.py

import sqlite3
import os

DB_PATH = 'deepfake_results.db'

# Create the database and table if it doesn't exist
def initialize_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS detections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                result TEXT NOT NULL,
                confidence REAL NOT NULL,
                timestamp TEXT NOT NULL
            )
        ''')
        conn.commit()

# Call this function once when module is imported
initialize_db()

# Insert new detection result
def insert_result(filename, result, confidence, timestamp):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO detections (filename, result, confidence, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (filename, result, confidence, str(timestamp)))
        conn.commit()
