import streamlit as st
import plotly.express as px
from datetime import datetime, timedelta


def render_ui(df):
    # Create tabs for different views
    tab1, tab2 = st.tabs(["📊 Dashboard", "🧹 Cleanup Insights"])
    
    with tab1:
        render_dashboard_tab(df)
    
    with tab2:
        render_cleanup_tab(df)


def render_dashboard_tab(df):
    st.sidebar.header("Filters")
    name_filter = st.sidebar.text_input("Filter by Name (contains, case-insensitive)")

    unique_folders = sorted(df["folder"].unique())
    unique_statuses = sorted(df["last_build_status"].unique())
    unique_types = sorted(df["type"].unique())

    folder_filter = st.sidebar.multiselect(
        "Filter by Folder", options=unique_folders, default=unique_folders
    )
    status_filter = st.sidebar.multiselect(
        "Filter by Last Build Status", options=unique_statuses, default=unique_statuses
    )
    type_filter = st.sidebar.multiselect(
        "Filter by Type", options=unique_types, default=unique_types
    )

    # --- Apply Filters ---
    filtered_df = df.copy()
    if name_filter:
        filtered_df = filtered_df[
            filtered_df["name"].str.contains(name_filter, case=False, na=False)
        ]
    if folder_filter:
        filtered_df = filtered_df[filtered_df["folder"].isin(folder_filter)]
    if status_filter:
        filtered_df = filtered_df[filtered_df["last_build_status"].isin(status_filter)]
    if type_filter:
        filtered_df = filtered_df[filtered_df["type"].isin(type_filter)]

    # --- Visualizations ---
    st.header("Build Status Overview")
    if not filtered_df.empty:
        status_counts = filtered_df["last_build_status"].value_counts()
        fig = px.pie(
            status_counts,
            values=status_counts.values,
            names=status_counts.index,
            title="Last Build Status Distribution",
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data matches the current filters.")

    # --- Display Data ---
    st.header("Filtered Jenkins Jobs")
    st.info(f"Displaying {len(filtered_df)} of {len(df)} total items.")
    st.dataframe(
        filtered_df,
        column_config={
            "url": st.column_config.LinkColumn("Job URL"),
            "last_build_url": st.column_config.LinkColumn("Last Build URL"),
        },
        use_container_width=True,
    )


def render_cleanup_tab(df):
    st.header("🧹 Jenkins Cleanup Insights")
    st.markdown("This page helps identify jobs that might need cleanup or attention.")
    
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
    st.markdown("Jobs that haven't been triggered for 60+ days:")
    
    # Filter for jobs with last build more than 60 days ago
    inactive_jobs = df[
        (df["days_since_last_build"] > 60) & 
        (df["days_since_last_build"].notna())
    ].copy()
    
    if not inactive_jobs.empty:
        st.warning(f"Found {len(inactive_jobs)} inactive jobs")
        
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
    inactive_jobs_count = len(df[(df["days_since_last_build"] > 60) & (df["days_since_last_build"].notna())])
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
        recommendations.append(f"**{inactive_jobs_count} inactive jobs** found - Consider archiving or removing jobs not used for 60+ days")
    
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
    if row["days_since_last_build"] and row["days_since_last_build"] > 60:
        return "🗑️ Consider removal - disabled and inactive"
    else:
        return "📋 Review - disabled but recently active"
