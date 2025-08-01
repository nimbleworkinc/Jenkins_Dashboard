import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from src.data_manager import init_db, get_cached_data, cache_data
from src.jenkins_api import get_all_jenkins_items
from src.ui import render_ui
from src.config import DashboardConfig

load_dotenv()

# Validate configuration
try:
    DashboardConfig.validate_config()
except ValueError as e:
    st.error(f"Configuration Error: {e}")
    st.error("Please check your .env file and ensure all required variables are set.")
    st.stop()

st.set_page_config(layout=DashboardConfig.PAGE_LAYOUT)

init_db()

# --- Main App Logic ---
df, last_sync_timestamp = get_cached_data()

# Store last sync time in session state for use in UI
if df is not None and not df.empty:
    if last_sync_timestamp:
        # Convert to configured timezone
        last_sync_time = pd.Timestamp.fromtimestamp(last_sync_timestamp, tz='UTC').tz_convert(DashboardConfig.TIMEZONE).strftime(DashboardConfig.TIMEZONE_DISPLAY_FORMAT)
    else:
        last_sync_time = "Unknown"
    st.session_state.last_sync_time = last_sync_time
    st.session_state.jobs_count = len(df)

# Check if we need to fetch data (no cached data or refresh requested)
if df is None or df.empty or st.session_state.get('refresh_data', False):
    if st.session_state.get('refresh_data', False):
        st.info("🔄 Refreshing data from Jenkins...")
    else:
        st.info("No cached data found. Fetching from Jenkins...")

    auth = HTTPBasicAuth(DashboardConfig.JENKINS_USER, DashboardConfig.JENKINS_TOKEN)
    
    with st.spinner("Fetching all jobs and pipelines... this may take a moment."):
        # Clear cache if this is a refresh request to ensure fresh data
        if st.session_state.get('refresh_data', False):
            get_all_jenkins_items.clear()
        
        # Suppress the function call display by using a try-except wrapper
        try:
            # Pass bypass_cache=True when refreshing to ensure fresh data
            bypass_cache = st.session_state.get('refresh_data', False)
            all_items = get_all_jenkins_items(DashboardConfig.JENKINS_BASE_URL, auth, bypass_cache)
        except Exception as e:
            st.error(f"Error fetching data: {e}")
            st.stop()
    
        if all_items:
            df = pd.DataFrame(all_items)
            cache_data(df)
            # Clear the refresh flag
            if 'refresh_data' in st.session_state:
                del st.session_state.refresh_data
            st.success(f"✅ Successfully synced {len(df)} jobs from Jenkins!")
            st.info("🔄 Refreshing dashboard with latest data...")
            st.rerun()
        else:
            st.warning("No items found or an error occurred.")
            st.stop()

if df is None or df.empty:
    st.warning("No data to display. Please refresh from Jenkins.")
    st.stop()

render_ui(df)
