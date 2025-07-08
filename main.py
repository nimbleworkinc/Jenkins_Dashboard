import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from src.data_manager import init_db, get_cached_data, cache_data
from src.jenkins_api import get_all_jenkins_items
from src.ui import render_ui

load_dotenv()

st.set_page_config(layout="wide")
st.title("Jenkins Jobs and Pipelines Dashboard")

init_db()

# --- Main App Logic ---
df = get_cached_data()

if st.sidebar.button("Refresh Data from Jenkins") or df is None or df.empty:
    if df is None or df.empty:
        st.info("No cached data found. Fetching from Jenkins...")

    jenkins_user = os.getenv("JENKINS_USER")
    jenkins_token = os.getenv("JENKINS_TOKEN")

    if not jenkins_user or not jenkins_token:
        st.error("Jenkins credentials not found in .env file.")
        st.stop()

    auth = HTTPBasicAuth(jenkins_user, jenkins_token)
    jenkins_base_url = os.getenv("JENKINS_BASE_URL")
    with st.spinner("Fetching all jobs and pipelines... this may take a moment."):
        all_items = get_all_jenkins_items(jenkins_base_url, auth)
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
