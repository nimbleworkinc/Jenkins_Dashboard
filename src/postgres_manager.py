import pandas as pd
import psycopg2
import psycopg2.extras
import time
from datetime import datetime, timezone
from src.config import DashboardConfig


class PostgreSQLManager:
    """PostgreSQL database manager for Jenkins Dashboard"""
    
    def __init__(self):
        self.connection_string = (
            f"postgresql://{DashboardConfig.POSTGRES_USER}:{DashboardConfig.POSTGRES_PASSWORD}"
            f"@{DashboardConfig.POSTGRES_HOST}:{DashboardConfig.POSTGRES_PORT}/{DashboardConfig.POSTGRES_DB}"
        )
    
    def get_connection(self):
        """Get database connection"""
        try:
            conn = psycopg2.connect(self.connection_string)
            return conn
        except psycopg2.Error as e:
            raise Exception(f"Failed to connect to PostgreSQL: {e}")
    
    def init_db(self):
        """Initialize database (tables are created by init script)"""
        try:
            conn = self.get_connection()
            conn.close()
            print("✅ PostgreSQL database initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize PostgreSQL database: {e}")
            raise
    
    def get_cached_data(self):
        """Get cached data from PostgreSQL"""
        try:
            conn = self.get_connection()
            
            # Get the data
            query = """
                SELECT name, url, type, description, last_build_status, last_build_url, folder,
                       is_disabled, last_build_date, last_successful_date, last_failed_date,
                       days_since_last_build, total_builds, success_count, failure_count,
                       success_rate, is_test_job, last_build_duration, last_successful_duration,
                       last_failed_duration, avg_build_duration, avg_successful_duration,
                       avg_failed_duration, min_build_duration, max_build_duration,
                       total_build_duration, owner_name, owner_email, other_tag, ownership_status, timestamp
                FROM jenkins_items
                ORDER BY name
            """
            
            df = pd.read_sql_query(query, conn)
            
            # Get the timestamp of when data was last cached
            timestamp_query = "SELECT timestamp FROM jenkins_items ORDER BY timestamp DESC LIMIT 1"
            cursor = conn.cursor()
            cursor.execute(timestamp_query)
            result = cursor.fetchone()
            last_sync_timestamp = result[0] if result else None
            cursor.close()
            
            # Handle data types and nulls
            if not df.empty:
                df["last_build_status"] = df["last_build_status"].fillna("Unknown")
                df["is_disabled"] = df["is_disabled"].fillna(False).astype(bool)
                df["is_test_job"] = df["is_test_job"].fillna(False).astype(bool)
                df["success_rate"] = df["success_rate"].fillna(0.0)
                # Ensure success_rate is within PostgreSQL DECIMAL(10,2) range
                df["success_rate"] = df["success_rate"].clip(-99999999.99, 99999999.99)
                
                # Debug: Check for any extreme values
                max_rate = df["success_rate"].max()
                min_rate = df["success_rate"].min()
                print(f"Debug: success_rate range - min: {min_rate}, max: {max_rate}")
                
                # Check for any infinite values
                if df["success_rate"].isin([float('inf'), float('-inf')]).any():
                    print("Warning: Found infinite values in success_rate, replacing with 0.0")
                    df["success_rate"] = df["success_rate"].replace([float('inf'), float('-inf')], 0.0)
                df["success_count"] = df["success_count"].fillna(0)
                df["failure_count"] = df["failure_count"].fillna(0)
                
                # Fill NaN values for duration columns
                duration_columns = [
                    "last_build_duration", "last_successful_duration", "last_failed_duration",
                    "avg_build_duration", "avg_successful_duration", "avg_failed_duration",
                    "min_build_duration", "max_build_duration", "total_build_duration"
                ]
                for col in duration_columns:
                    df[col] = df[col].fillna(0)
            
            conn.close()
            return df, last_sync_timestamp
            
        except Exception as e:
            print(f"❌ Error getting cached data from PostgreSQL: {e}")
            return None, None
    
    def cache_data(self, df):
        """Cache data to PostgreSQL"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Clear existing data
            cursor.execute("DELETE FROM jenkins_items")
            
            # Prepare data for insertion
            df_copy = df.copy()
            df_copy["timestamp"] = time.time()
            
            # Convert datetime columns to proper format and handle NaT values
            datetime_columns = ["last_build_date", "last_successful_date", "last_failed_date"]
            for col in datetime_columns:
                if col in df_copy.columns:
                    # Convert to datetime and replace NaT with None
                    df_copy[col] = pd.to_datetime(df_copy[col], utc=True, errors='coerce')
                    df_copy[col] = df_copy[col].replace({pd.NaT: None})
            
            # Insert data using executemany for better performance
            columns = [
                "name", "url", "type", "description", "last_build_status", "last_build_url", 
                "folder", "is_disabled", "last_build_date", "last_successful_date", 
                "last_failed_date", "days_since_last_build", "total_builds", "success_count", 
                "failure_count", "success_rate", "is_test_job", "last_build_duration", 
                "last_successful_duration", "last_failed_duration", "avg_build_duration", 
                "avg_successful_duration", "avg_failed_duration", "min_build_duration", 
                "max_build_duration", "total_build_duration", "owner_name", "owner_email", 
                "other_tag", "ownership_status", "timestamp"
            ]
            
            # Prepare data tuples with proper data type handling
            data_tuples = []
            for _, row in df_copy.iterrows():
                data_tuple = []
                for col in columns:
                    value = row[col]
                    
                    # Handle NaN/NaT values
                    if pd.isna(value) or (hasattr(value, 'value') and pd.isna(value.value)):
                        data_tuple.append(None)
                    else:
                        # Handle numeric fields specifically
                        if col == 'success_rate':
                            # Ensure success_rate is within PostgreSQL DECIMAL(10,2) range
                            try:
                                rate = float(value)
                                if rate > 99999999.99:
                                    rate = 99999999.99
                                elif rate < -99999999.99:
                                    rate = -99999999.99
                                data_tuple.append(rate)
                            except (ValueError, TypeError):
                                data_tuple.append(0.0)
                        elif col in ['avg_build_duration', 'avg_successful_duration', 'avg_failed_duration']:
                            # Handle other numeric fields
                            try:
                                val = float(value)
                                if val > 99999999.99:
                                    val = 99999999.99
                                elif val < -99999999.99:
                                    val = -99999999.99
                                data_tuple.append(val)
                            except (ValueError, TypeError):
                                data_tuple.append(0.0)
                        else:
                            data_tuple.append(value)
                data_tuples.append(tuple(data_tuple))
            
            # Insert data
            insert_query = f"""
                INSERT INTO jenkins_items ({', '.join(columns)})
                VALUES ({', '.join(['%s'] * len(columns))})
            """
            
            psycopg2.extras.execute_batch(cursor, insert_query, data_tuples, page_size=1000)
            
            conn.commit()
            cursor.close()
            conn.close()
            
            print(f"✅ Successfully cached {len(df)} jobs to PostgreSQL")
            
        except Exception as e:
            print(f"❌ Error caching data to PostgreSQL: {e}")
            raise
    
    def get_database_stats(self):
        """Get database statistics"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Get basic stats
            cursor.execute("SELECT COUNT(*) FROM jenkins_items")
            total_jobs = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM jenkins_items WHERE is_disabled = TRUE")
            disabled_jobs = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM jenkins_items WHERE is_test_job = TRUE")
            test_jobs = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM jenkins_items WHERE description IS NULL OR description = ''")
            jobs_without_desc = cursor.fetchone()[0]
            
            cursor.execute("SELECT MAX(timestamp) FROM jenkins_items")
            last_sync = cursor.fetchone()[0]
            
            cursor.close()
            conn.close()
            
            return {
                "total_jobs": total_jobs,
                "disabled_jobs": disabled_jobs,
                "test_jobs": test_jobs,
                "jobs_without_description": jobs_without_desc,
                "last_sync": last_sync
            }
            
        except Exception as e:
            print(f"❌ Error getting database stats: {e}")
            return None
    
    def cleanup_old_data(self, days_to_keep=90):
        """Clean up old data (optional maintenance function)"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cutoff_timestamp = time.time() - (days_to_keep * 24 * 60 * 60)
            
            cursor.execute(
                "DELETE FROM jenkins_items WHERE timestamp < %s",
                (cutoff_timestamp,)
            )
            
            deleted_count = cursor.rowcount
            conn.commit()
            cursor.close()
            conn.close()
            
            print(f"✅ Cleaned up {deleted_count} old records (older than {days_to_keep} days)")
            
        except Exception as e:
            print(f"❌ Error cleaning up old data: {e}")
            raise 