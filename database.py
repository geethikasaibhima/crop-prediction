"""
SQLite3 Database module for Smart Crop Prediction System.
Provides clean, parameterized operations to initialize the database,
save prediction records, and retrieve prediction history.
"""

import os
import sqlite3
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'crop_prediction.db')


def get_db_connection():
    """Returns a new SQLite3 connection with row_factory configured."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initializes the SQLite database and ensures the predictions table exists."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                N REAL NOT NULL,
                P REAL NOT NULL,
                K REAL NOT NULL,
                temperature REAL NOT NULL,
                humidity REAL NOT NULL,
                ph REAL NOT NULL,
                rainfall REAL NOT NULL,
                predicted_crop TEXT NOT NULL,
                timestamp TEXT NOT NULL
            );
        """)
        conn.commit()
        print(f"[SQLite] Database initialized at: {DB_PATH}")
    except sqlite3.Error as e:
        print(f"[SQLite Error] Failed to initialize database: {e}")
    finally:
        conn.close()


def save_prediction(record):
    """
    Saves a successful prediction record into SQLite3 using parameterized queries.
    Expects dict with keys: N, P, K, temperature, humidity, ph, rainfall, predicted_crop.
    Returns True if successfully saved, False otherwise.
    """
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    query = """
        INSERT INTO predictions (
            N, P, K, temperature, humidity, ph, rainfall, predicted_crop, timestamp
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    params = (
        float(record['N']),
        float(record['P']),
        float(record['K']),
        round(float(record['temperature']), 2),
        round(float(record['humidity']), 2),
        round(float(record['ph']), 2),
        round(float(record['rainfall']), 2),
        str(record['predicted_crop']),
        timestamp
    )

    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"[SQLite Error] Failed to insert prediction: {e}")
        return False
    finally:
        conn.close()


def get_predictions(limit=50):
    """
    Retrieves previous prediction records from SQLite3, ordered newest first (id DESC).
    Returns a list of dicts.
    """
    query = """
        SELECT id, N, P, K, temperature, humidity, ph, rainfall, predicted_crop, timestamp
        FROM predictions
        ORDER BY id DESC
        LIMIT ?
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, (limit,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    except sqlite3.Error as e:
        print(f"[SQLite Error] Failed to retrieve predictions: {e}")
        return []
    finally:
        conn.close()
