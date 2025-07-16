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
st.title(DashboardConfig.DASHBOARD_TITLE)

init_db()

# --- Main App Logic ---
df = get_cached_data()

if st.sidebar.button("Refresh Data from Jenkins") or df is None or df.empty:
    if df is None or df.empty:
        st.info("No cached data found. Fetching from Jenkins...")

    auth = HTTPBasicAuth(DashboardConfig.JENKINS_USER, DashboardConfig.JENKINS_TOKEN)
    
    with st.spinner("Fetching all jobs and pipelines... this may take a moment."):
        all_items = get_all_jenkins_items(DashboardConfig.JENKINS_BASE_URL, auth)
        if all_items:
            df = pd.DataFrame(all_items)
            cache_data(df)
            st.success(f"Found and cached {len(df)} items.")
            st.rerun()
        else:
            st.warning("No items found or an error occurred.")
            st.stop()

if df is None or df.empty:
    st.warning("No data to display. Please refresh from Jenkins.")
    st.stop()

render_ui(df)
