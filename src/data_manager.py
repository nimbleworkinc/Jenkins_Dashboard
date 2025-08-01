import pandas as pd
import sqlite3
import time
from src.config import DashboardConfig

DB_FILE = DashboardConfig.DB_FILE

# Import PostgreSQL manager if needed
try:
    from src.postgres_manager import PostgreSQLManager
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False


def init_db():
    """Initialize database based on configuration"""
    if DashboardConfig.DB_TYPE == "postgresql" and POSTGRES_AVAILABLE:
        # Use PostgreSQL
        postgres_manager = PostgreSQLManager()
        postgres_manager.init_db()
    else:
        # Use SQLite (default)
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS jenkins_items
            (name TEXT, url TEXT, type TEXT, description TEXT, last_build_status TEXT, 
             last_build_url TEXT, folder TEXT, timestamp REAL,
             is_disabled INTEGER, last_build_date TEXT, last_successful_date TEXT,
             last_failed_date TEXT, days_since_last_build INTEGER, total_builds INTEGER,
             success_count INTEGER, failure_count INTEGER, success_rate REAL,
             is_test_job INTEGER, last_build_duration INTEGER, last_successful_duration INTEGER,
             last_failed_duration INTEGER, avg_build_duration REAL, avg_successful_duration REAL,
             avg_failed_duration REAL, min_build_duration INTEGER, max_build_duration INTEGER,
             total_build_duration INTEGER, owner_name TEXT, owner_email TEXT, other_tag TEXT, 
             ownership_status TEXT, last_editor TEXT, last_user TEXT)
        """)
        conn.commit()
        conn.close()


def get_cached_data():
    """Get cached data based on database configuration"""
    if DashboardConfig.DB_TYPE == "postgresql" and POSTGRES_AVAILABLE:
        # Use PostgreSQL
        postgres_manager = PostgreSQLManager()
        return postgres_manager.get_cached_data()
    else:
        # Use SQLite (default)
        conn = sqlite3.connect(DB_FILE)
        try:
            # Get the data
            df = pd.read_sql_query(
                "SELECT name, url, type, description, last_build_status, last_build_url, folder, "
                "is_disabled, last_build_date, last_successful_date, last_failed_date, "
                "days_since_last_build, total_builds, success_count, failure_count, "
                "success_rate, is_test_job, last_build_duration, last_successful_duration, "
                "last_failed_duration, avg_build_duration, avg_successful_duration, "
                "avg_failed_duration, min_build_duration, max_build_duration, "
                "total_build_duration, owner_name, owner_email, other_tag, ownership_status, last_editor, last_user FROM jenkins_items",
                conn,
            )
            
            # Get the timestamp of when data was last cached
            timestamp_result = conn.execute("SELECT timestamp FROM jenkins_items LIMIT 1").fetchone()
            last_sync_timestamp = timestamp_result[0] if timestamp_result else None
            
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
            
            return df, last_sync_timestamp
        except (pd.io.sql.DatabaseError, sqlite3.OperationalError):
            return None, None
        finally:
            conn.close()


def cache_data(df):
    """Cache data based on database configuration"""
    if DashboardConfig.DB_TYPE == "postgresql" and POSTGRES_AVAILABLE:
        # Use PostgreSQL
        postgres_manager = PostgreSQLManager()
        postgres_manager.cache_data(df)
    else:
        # Use SQLite (default)
        conn = sqlite3.connect(DB_FILE)
        df["timestamp"] = time.time()
        df.to_sql("jenkins_items", conn, if_exists="replace", index=False)
        conn.close()
