import pandas as pd
import sqlite3
import time
from src.config import DashboardConfig

DB_FILE = DashboardConfig.DB_FILE


def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS jenkins_items
        (name TEXT, url TEXT, type TEXT, last_build_status TEXT, 
         last_build_url TEXT, folder TEXT, timestamp REAL,
         is_disabled INTEGER, last_build_date TEXT, last_successful_date TEXT,
         last_failed_date TEXT, days_since_last_build INTEGER, total_builds INTEGER,
         success_count INTEGER, failure_count INTEGER, success_rate REAL,
         is_test_job INTEGER, last_build_duration INTEGER, last_successful_duration INTEGER,
         last_failed_duration INTEGER, avg_build_duration REAL, avg_successful_duration REAL,
         avg_failed_duration REAL, min_build_duration INTEGER, max_build_duration INTEGER,
         total_build_duration INTEGER)
    """)
    conn.commit()
    conn.close()


def get_cached_data():
    conn = sqlite3.connect(DB_FILE)
    try:
        df = pd.read_sql_query(
            "SELECT name, url, type, last_build_status, last_build_url, folder, "
            "is_disabled, last_build_date, last_successful_date, last_failed_date, "
            "days_since_last_build, total_builds, success_count, failure_count, "
            "success_rate, is_test_job, last_build_duration, last_successful_duration, "
            "last_failed_duration, avg_build_duration, avg_successful_duration, "
            "avg_failed_duration, min_build_duration, max_build_duration, "
            "total_build_duration FROM jenkins_items",
            conn,
        )
        df["last_build_status"] = df["last_build_status"].fillna("Unknown")
        # Convert boolean columns
        df["is_disabled"] = df["is_disabled"].fillna(False).astype(bool)
        df["is_test_job"] = df["is_test_job"].fillna(False).astype(bool)
        # Fill NaN values for numeric columns
        df["success_rate"] = df["success_rate"].fillna(0.0)
        df["success_count"] = df["success_count"].fillna(0)
        df["failure_count"] = df["failure_count"].fillna(0)
        # Fill NaN values for duration columns
        duration_columns = ["last_build_duration", "last_successful_duration", "last_failed_duration",
                          "avg_build_duration", "avg_successful_duration", "avg_failed_duration",
                          "min_build_duration", "max_build_duration", "total_build_duration"]
        for col in duration_columns:
            df[col] = df[col].fillna(0)
        return df
    except (pd.io.sql.DatabaseError, sqlite3.OperationalError):
        return None
    finally:
        conn.close()


def cache_data(df):
    conn = sqlite3.connect(DB_FILE)
    df["timestamp"] = time.time()
    df.to_sql("jenkins_items", conn, if_exists="replace", index=False)
    conn.close()
