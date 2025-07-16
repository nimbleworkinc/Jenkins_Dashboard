import streamlit as st
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd
from src.config import DashboardConfig


def render_ui(df):
    # Create tabs for different views
    tab1, tab2 = st.tabs(["📊 Dashboard", "🧹 Cleanup Insights"])
    
    with tab1:
        render_dashboard_tab(df)
    
    with tab2:
        render_cleanup_tab(df)


def render_dashboard_tab(df):
    # Enhanced sidebar with better organization
    with st.sidebar:
        st.header("🔍 Search & Filters")
        
        # Smart search with autocomplete suggestions
        search_term = st.text_input(
            "🔎 Quick Search",
            placeholder="Search by job name, folder, or status...",
            help="Type to search across all fields"
        )
        
        # Advanced search options
        with st.expander("🔧 Advanced Search", expanded=False):
            name_filter = st.text_input("Filter by Name (exact match)")
            folder_filter = st.text_input("Filter by Folder (exact match)")
            status_filter = st.selectbox("Filter by Status", ["All"] + sorted(df["last_build_status"].unique().tolist()))
        
        st.markdown("---")
        st.header("📂 Quick Filters")
        
        # Simple dropdown for folder filter (no search, show all)
        unique_folders = sorted(df["folder"].unique())
        folder_filter_multiselect = st.multiselect(
            "📁 Filter by Folder",
            options=unique_folders,
            default=[],  # No default selection - show all folders
            help="Select specific folders to include (leave empty to show all)"
        )
        
        # Simple dropdown for status filter
        unique_statuses = sorted(df["last_build_status"].unique())
        status_filter_multiselect = st.multiselect(
            "🎯 Filter by Status",
            options=unique_statuses,
            default=[],  # No default selection - show all statuses
            help="Select specific statuses to include (leave empty to show all)"
        )
        
        # Pagination controls
        st.markdown("---")
        st.header("📄 Pagination")
        items_per_page = st.selectbox("Items per page", [25, 50, 100, 200], 
                                    index=[25, 50, 100, 200].index(DashboardConfig.ITEMS_PER_PAGE_DEFAULT))
        
        # Show current filter summary
        st.markdown("---")
        st.header("📊 Current Filters")
        if search_term:
            st.info(f"🔍 Search: '{search_term}'")
        if folder_filter_multiselect:
            st.info(f"📁 Folders: {len(folder_filter_multiselect)} selected")
        if status_filter_multiselect:
            st.info(f"🎯 Status: {len(status_filter_multiselect)} selected")
        
        # Show total items info
        total_items = len(df)
        st.info(f"📊 Total Jobs: {total_items}")

    # Apply filters
    filtered_df = apply_filters(df, search_term, name_filter, folder_filter, status_filter, 
                               folder_filter_multiselect, status_filter_multiselect, [])
    
    # Enhanced visualizations
    render_enhanced_visualizations(filtered_df, len(filtered_df), total_items)
    
    # Enhanced data display with integrated pagination
    render_enhanced_data_table(filtered_df, len(filtered_df), items_per_page)


def apply_filters(df, search_term, name_filter, folder_filter, status_filter, 
                 folder_filter_multiselect, status_filter_multiselect, type_filter):
    """Apply all filters to the dataframe"""
    filtered_df = df.copy()
    
    # Quick search across all fields
    if search_term:
        search_mask = (
            filtered_df["name"].str.contains(search_term, case=False, na=False) |
            filtered_df["folder"].str.contains(search_term, case=False, na=False) |
            filtered_df["last_build_status"].str.contains(search_term, case=False, na=False) |
            filtered_df["type"].str.contains(search_term, case=False, na=False)
        )
        filtered_df = filtered_df[search_mask]
    
    # Advanced filters
    if name_filter:
        filtered_df = filtered_df[filtered_df["name"].str.contains(name_filter, case=False, na=False)]
    if folder_filter:
        filtered_df = filtered_df[filtered_df["folder"].str.contains(folder_filter, case=False, na=False)]
    if status_filter and status_filter != "All":
        filtered_df = filtered_df[filtered_df["last_build_status"] == status_filter]
    
    # Multi-select filters (only apply if selections are made)
    if folder_filter_multiselect:
        filtered_df = filtered_df[filtered_df["folder"].isin(folder_filter_multiselect)]
    if status_filter_multiselect:
        filtered_df = filtered_df[filtered_df["last_build_status"].isin(status_filter_multiselect)]
    
    return filtered_df


def render_enhanced_visualizations(df, total_filtered_items, total_items):
    """Render enhanced visualizations with better styling"""
    st.header("📊 Build Status Overview")
    
    if not df.empty:
        # KPI Cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            success_count = len(df[df["last_build_status"] == "SUCCESS"])
            success_rate = (success_count / len(df)) * 100 if len(df) > 0 else 0
            st.metric("✅ Success Rate", f"{success_rate:.1f}%", f"{success_count} jobs")
        
        with col2:
            failure_count = len(df[df["last_build_status"] == "FAILURE"])
            failure_rate = (failure_count / len(df)) * 100 if len(df) > 0 else 0
            st.metric("❌ Failure Rate", f"{failure_rate:.1f}%", f"{failure_count} jobs")
        
        with col3:
            inactive_count = len(df[df["days_since_last_build"] > DashboardConfig.INACTIVE_JOB_THRESHOLD_DAYS]) if "days_since_last_build" in df.columns else 0
            st.metric("⏰ Inactive Jobs", inactive_count, f">{DashboardConfig.INACTIVE_JOB_THRESHOLD_DAYS} days")
        
        with col4:
            disabled_count = len(df[df["is_disabled"] == True]) if "is_disabled" in df.columns else 0
            st.metric("🚫 Disabled Jobs", disabled_count)
        
        # Show filtered vs total info
        if total_filtered_items != total_items:
            st.info(f"📊 Showing {total_filtered_items} of {total_items} total jobs (filtered)")
        else:
            st.info(f"📊 Showing all {total_items} jobs")
        
        # Enhanced pie chart
        status_counts = df["last_build_status"].value_counts()
        fig = px.pie(
            status_counts,
            values=status_counts.values,
            names=status_counts.index,
            title=f"Build Status Distribution ({total_filtered_items} jobs)",
            color_discrete_map={
                "SUCCESS": "#00FF00",
                "FAILURE": "#FF0000", 
                "UNSTABLE": "#FFFF00",
                "ABORTED": "#808080",
                "IN_PROGRESS": "#0000FF",
                "Not Built": "#FFA500"
            }
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data matches the current filters.")


def render_enhanced_data_table(df, total_filtered_items, items_per_page):
    """Render enhanced data table with integrated pagination and cleaner columns"""
    st.header("📋 Jenkins Jobs")
    
    # Pagination controls integrated near the table
    total_pages = (total_filtered_items + items_per_page - 1) // items_per_page
    
    if total_pages > 1:
        col1, col2, col3, col4 = st.columns([2, 1, 1, 2])
        with col2:
            current_page = st.selectbox(f"📄 Page", range(1, total_pages + 1), index=0)
        with col3:
            st.write(f"of {total_pages}")
    else:
        current_page = 1
    
    start_idx = (current_page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    paginated_df = df.iloc[start_idx:end_idx]
    
    # Summary info
    start_item = (current_page - 1) * items_per_page + 1
    end_item = min(current_page * items_per_page, total_filtered_items)
    
    st.info(f"Showing {start_item}-{end_item} of {total_filtered_items} jobs")
    
    if not paginated_df.empty:
        # Select only the columns we want to display
        display_columns = [
            "name", "folder", "last_build_status", "success_rate",
            "days_since_last_build", "total_builds", "url"
        ]
        
        # Filter dataframe to only show selected columns
        display_df = paginated_df[display_columns].copy()
        
        # Enhanced dataframe with cleaner columns
        st.dataframe(
            display_df,
            column_config={
                "url": st.column_config.LinkColumn("🔗 Job URL"),
                "last_build_status": st.column_config.SelectboxColumn(
                    "🎯 Status",
                    options=sorted(df["last_build_status"].unique()),
                    required=True
                ),
                "success_rate": st.column_config.NumberColumn(
                    "📊 Success Rate",
                    format="%.1f%%",
                    help="Percentage of successful builds",
                    min_value=0,
                    max_value=100
                ),
                "days_since_last_build": st.column_config.NumberColumn(
                    "📅 Days Since Last Build",
                    format="%d days",
                    help="Number of days since the last build"
                ),
                "total_builds": st.column_config.NumberColumn(
                    "🔢 Total Builds",
                    format="%d",
                    help="Total number of builds for this job"
                ),
            },
            use_container_width=True,
            hide_index=True
        )
    else:
        st.warning("No jobs found matching the current filters.")


def render_cleanup_tab(df):
    st.header("🧹 Jenkins Cleanup Insights")
    st.markdown("This page helps identify jobs that might need cleanup or attention.")
    
    # Debug: Check if required columns exist
    required_columns = ["is_test_job", "is_disabled", "days_since_last_build"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        st.error(f"Missing required columns: {missing_columns}. Please refresh data from Jenkins.")
        return
    
    # Create sub-tabs for different cleanup categories
    cleanup_tab1, cleanup_tab2, cleanup_tab3, cleanup_tab4 = st.tabs([
        "🧪 Test Jobs", "⏰ Inactive Jobs", "🚫 Disabled Jobs", "📋 Summary"
    ])
    
    with cleanup_tab1:
        render_test_jobs_section(df)
    
    with cleanup_tab2:
        render_inactive_jobs_section(df)
    
    with cleanup_tab3:
        render_disabled_jobs_section(df)
    
    with cleanup_tab4:
        render_cleanup_summary(df)


def render_test_jobs_section(df):
    st.subheader("🧪 Test Jobs")
    st.markdown("Jobs that appear to be test/demo/temporary pipelines:")
    
    test_jobs = df[df["is_test_job"] == True].copy()
    
    if not test_jobs.empty:
        st.info(f"Found {len(test_jobs)} potential test jobs")
        
        # Add search for test jobs
        test_search = st.text_input("🔍 Search test jobs...", placeholder="Filter test jobs by name or folder")
        if test_search:
            test_jobs = test_jobs[
                test_jobs["name"].str.contains(test_search, case=False, na=False) |
                test_jobs["folder"].str.contains(test_search, case=False, na=False)
            ]
            st.info(f"Showing {len(test_jobs)} test jobs matching '{test_search}'")
        
        # Add recommendations
        test_jobs["recommendation"] = test_jobs.apply(
            lambda row: get_test_job_recommendation(row), axis=1
        )
        
        st.dataframe(
            test_jobs[["name", "folder", "last_build_status", "days_since_last_build", "total_builds", "recommendation", "url"]],
            column_config={
                "url": st.column_config.LinkColumn("Job URL"),
                "days_since_last_build": st.column_config.NumberColumn("Days Since Last Build", format="%d"),
                "total_builds": st.column_config.NumberColumn("Total Builds", format="%d"),
            },
            use_container_width=True,
        )
    else:
        st.success("No test jobs found! 🎉")


def render_inactive_jobs_section(df):
    st.subheader("⏰ Inactive Jobs")
    st.markdown(f"Jobs that haven't been triggered for {DashboardConfig.INACTIVE_JOB_THRESHOLD_DAYS}+ days:")
    
    # Filter for jobs with last build more than threshold days ago
    inactive_jobs = df[
        (df["days_since_last_build"] > DashboardConfig.INACTIVE_JOB_THRESHOLD_DAYS) & 
        (df["days_since_last_build"].notna())
    ].copy()
    
    if not inactive_jobs.empty:
        st.warning(f"Found {len(inactive_jobs)} inactive jobs")
        
        # Add search for inactive jobs
        inactive_search = st.text_input("🔍 Search inactive jobs...", placeholder="Filter inactive jobs by name or folder")
        if inactive_search:
            inactive_jobs = inactive_jobs[
                inactive_jobs["name"].str.contains(inactive_search, case=False, na=False) |
                inactive_jobs["folder"].str.contains(inactive_search, case=False, na=False)
            ]
            st.info(f"Showing {len(inactive_jobs)} inactive jobs matching '{inactive_search}'")
        
        # Add recommendations
        inactive_jobs["recommendation"] = inactive_jobs.apply(
            lambda row: get_inactive_job_recommendation(row), axis=1
        )
        
        # Sort by days since last build (most inactive first)
        inactive_jobs = inactive_jobs.sort_values("days_since_last_build", ascending=False)
        
        st.dataframe(
            inactive_jobs[["name", "folder", "last_build_status", "days_since_last_build", "total_builds", "recommendation", "url"]],
            column_config={
                "url": st.column_config.LinkColumn("Job URL"),
                "days_since_last_build": st.column_config.NumberColumn("Days Since Last Build", format="%d"),
                "total_builds": st.column_config.NumberColumn("Total Builds", format="%d"),
            },
            use_container_width=True,
        )
    else:
        st.success("No inactive jobs found! 🎉")


def render_disabled_jobs_section(df):
    st.subheader("🚫 Disabled Jobs")
    st.markdown("Jobs that are currently disabled:")
    
    disabled_jobs = df[df["is_disabled"] == True].copy()
    
    if not disabled_jobs.empty:
        st.info(f"Found {len(disabled_jobs)} disabled jobs")
        
        # Add search for disabled jobs
        disabled_search = st.text_input("🔍 Search disabled jobs...", placeholder="Filter disabled jobs by name or folder")
        if disabled_search:
            disabled_jobs = disabled_jobs[
                disabled_jobs["name"].str.contains(disabled_search, case=False, na=False) |
                disabled_jobs["folder"].str.contains(disabled_search, case=False, na=False)
            ]
            st.info(f"Showing {len(disabled_jobs)} disabled jobs matching '{disabled_search}'")
        
        # Add recommendations
        disabled_jobs["recommendation"] = disabled_jobs.apply(
            lambda row: get_disabled_job_recommendation(row), axis=1
        )
        
        st.dataframe(
            disabled_jobs[["name", "folder", "last_build_status", "days_since_last_build", "total_builds", "recommendation", "url"]],
            column_config={
                "url": st.column_config.LinkColumn("Job URL"),
                "days_since_last_build": st.column_config.NumberColumn("Days Since Last Build", format="%d"),
                "total_builds": st.column_config.NumberColumn("Total Builds", format="%d"),
            },
            use_container_width=True,
        )
    else:
        st.success("No disabled jobs found! 🎉")


def render_cleanup_summary(df):
    st.subheader("📋 Cleanup Summary")
    
    # Calculate statistics
    total_jobs = len(df)
    test_jobs_count = len(df[df["is_test_job"] == True])
    inactive_jobs_count = len(df[(df["days_since_last_build"] > DashboardConfig.INACTIVE_JOB_THRESHOLD_DAYS) & (df["days_since_last_build"].notna())])
    disabled_jobs_count = len(df[df["is_disabled"] == True])
    
    # Create summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Jobs", total_jobs)
    
    with col2:
        st.metric("Test Jobs", test_jobs_count, delta=f"{test_jobs_count/total_jobs*100:.1f}%")
    
    with col3:
        st.metric("Inactive Jobs", inactive_jobs_count, delta=f"{inactive_jobs_count/total_jobs*100:.1f}%")
    
    with col4:
        st.metric("Disabled Jobs", disabled_jobs_count, delta=f"{disabled_jobs_count/total_jobs*100:.1f}%")
    
    # Recommendations
    st.subheader("🎯 Cleanup Recommendations")
    
    recommendations = []
    
    if test_jobs_count > 0:
        recommendations.append(f"**{test_jobs_count} test jobs** found - Consider reviewing and removing obsolete test pipelines")
    
    if inactive_jobs_count > 0:
        recommendations.append(f"**{inactive_jobs_count} inactive jobs** found - Consider archiving or removing jobs not used for {DashboardConfig.INACTIVE_JOB_THRESHOLD_DAYS}+ days")
    
    if disabled_jobs_count > 0:
        recommendations.append(f"**{disabled_jobs_count} disabled jobs** found - Review if these should be re-enabled or removed")
    
    if not recommendations:
        st.success("🎉 Your Jenkins instance looks clean! No immediate cleanup actions needed.")
    else:
        for rec in recommendations:
            st.markdown(f"• {rec}")


def get_test_job_recommendation(row):
    """Generate recommendation for test jobs based on their characteristics"""
    if row["days_since_last_build"] and row["days_since_last_build"] > 30:
        return "🔄 Consider removing - inactive test job"
    elif row["total_builds"] < 5:
        return "⚠️ Review - low build count test job"
    else:
        return "📋 Review - active test job"


def get_inactive_job_recommendation(row):
    """Generate recommendation for inactive jobs"""
    if row["days_since_last_build"] > 180:
        return "🗑️ Strong candidate for removal - very old"
    elif row["days_since_last_build"] > 90:
        return "📋 Review for archiving - moderately old"
    else:
        return "👀 Monitor - recently inactive"


def get_disabled_job_recommendation(row):
    """Generate recommendation for disabled jobs"""
    if row["days_since_last_build"] and row["days_since_last_build"] > DashboardConfig.INACTIVE_JOB_THRESHOLD_DAYS:
        return "🗑️ Consider removal - disabled and inactive"
    else:
        return "📋 Review - disabled but recently active"
