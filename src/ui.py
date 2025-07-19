import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd
from src.config import DashboardConfig

# Custom CSS for modern styling
def load_custom_css():
    st.markdown("""
    <style>
    /* Modern Color Palette - Clean White-Black-Grey Theme with Better Contrast */
    :root {
        --primary-color: #000000;
        --primary-dark: #000000;
        --secondary-color: #1f2937;
        --accent-color: #3b82f6;
        --success-color: #059669;
        --warning-color: #d97706;
        --error-color: #dc2626;
        --background-light: #f3f4f6;
        --background-dark: #1f2937;
        --text-primary: #000000;
        --text-secondary: #374151;
        --border-color: #d1d5db;
        --card-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
    }
    
    /* Global Styles */
    .main {
        background: #1f2937;
        min-height: 100vh;
    }
    
    .stApp {
        background: #1f2937;
    }
    
    /* Modern Header */
    .modern-header {
        padding: 1rem 2rem;
        margin: 0.5rem 0;
    }
    
    .modern-header h1 {
        color: #ffffff;
        font-size: 3.5rem;
        font-weight: 800;
        margin: 0;
        text-align: center;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .modern-header p {
        color: #e5e7eb;
        text-align: center;
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
    }
    
    /* Modern Navigation */
    .nav-container {
        margin: 1rem 0;
    }
    
    /* Simple Section Headers */
    .section-header {
        color: #ffffff;
        font-size: 1.6rem;
        font-weight: 600;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #ffffff;
    }
    
    .section-header h2 {
        margin: 0;
        color: #ffffff;
        font-size: 1.6rem;
        font-weight: 600;
    }
    
    .section-header p {
        color: #e5e7eb;
        margin: 0.5rem 0 0 0;
        font-size: 1rem;
        font-weight: 400;
    }
    
    /* Enhanced Sidebar */
    .sidebar .sidebar-content {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem;
        box-shadow: var(--card-shadow);
        border: 1px solid var(--border-color);
    }
    
    /* Custom Metric Styling - Fixed for better visibility */
    .stMetric {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid var(--border-color);
        box-shadow: var(--card-shadow);
    }
    
    .stMetric > div {
        color: #000000 !important;
    }
    
    .stMetric label {
        color: #000000 !important;
        font-weight: 600 !important;
    }
    
    .stMetric [data-testid="metric-container"] {
        color: #000000 !important;
    }
    
    /* Enhanced Charts */
    .chart-container {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: var(--card-shadow);
        border: 1px solid var(--border-color);
    }
    
    /* Status Badges */
    .status-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .status-success {
        background: rgba(5, 150, 105, 0.1);
        color: var(--success-color);
        border: 1px solid rgba(5, 150, 105, 0.2);
    }
    
    .status-failure {
        background: rgba(220, 38, 38, 0.1);
        color: var(--error-color);
        border: 1px solid rgba(220, 38, 38, 0.2);
    }
    
    .status-unstable {
        background: rgba(217, 119, 6, 0.1);
        color: var(--warning-color);
        border: 1px solid rgba(217, 119, 6, 0.2);
    }
    
    /* Loading Animation */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(0, 0, 0, 0.1);
        border-radius: 50%;
        border-top-color: var(--accent-color);
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .modern-header h1 {
            font-size: 2rem;
        }
        
        .section-header {
            font-size: 1.5rem;
        }
    }
    
    /* Enhanced Tab Navigation - Main and Sub Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        margin-bottom: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        border: 1px solid var(--border-color);
        color: #000000 !important;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.2s ease;
        min-width: 120px;
        text-align: center;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #f9fafb;
        color: #000000 !important;
        transform: translateY(-1px);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #1f2937;
        color: white !important;
        border-color: #1f2937;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        transform: translateY(-2px);
    }
    
    /* Main Navigation Tabs - Larger and more prominent */
    .stTabs:first-of-type [data-baseweb="tab"] {
        padding: 1rem 2rem;
        font-size: 1.1rem;
        font-weight: 700;
        min-width: 160px;
        background: linear-gradient(135deg, #ffffff 0%, #f9fafb 100%);
    }
    
    .stTabs:first-of-type [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #1f2937 0%, #374151 100%);
        color: white !important;
        border: 2px solid #ffffff;
    }
    }
    
    .stTabs [data-baseweb="tab"] span {
        color: inherit !important;
    }
    
    /* Fix radio button text visibility */
    .stRadio > label {
        color: #000000 !important;
        font-weight: 500 !important;
    }
    
    .stRadio > div > div > div > label {
        color: #000000 !important;
        font-weight: 500 !important;
    }
    
    /* Fix any other text elements that might be light */
    .stMarkdown, .stText {
        color: #ffffff !important;
    }
    
    .stMarkdown p, .stText p {
        color: #e5e7eb !important;
    }
    
    /* Make bullet points and lists more visible */
    .stMarkdown ul, .stMarkdown ol {
        color: #e5e7eb !important;
    }
    
    .stMarkdown li {
        color: #e5e7eb !important;
    }
    
    /* Settings Expander Styling */
    .streamlit-expanderHeader {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 8px !important;
        color: #ffffff !important;
        font-weight: 500 !important;
        padding: 0.5rem 1rem !important;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: rgba(255, 255, 255, 0.15) !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
    }
    
    .streamlit-expanderContent {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        margin-top: 0.5rem !important;
        padding: 1rem !important;
    }
    
    /* Disabled button styling */
    .stButton > button:disabled {
        background-color: #6b7280 !important;
        color: #9ca3af !important;
        cursor: not-allowed !important;
    }
    </style>
    """, unsafe_allow_html=True)


def render_ui(df):
    # Load custom CSS
    load_custom_css()
    
    # Modern header with gradient background - Single title only
    from src.config import DashboardConfig
    
    st.markdown(f"""
    <div class="modern-header">
        <h1>🚀 {DashboardConfig.DASHBOARD_TITLE}</h1>
        <p style="color: #ffffff;">Comprehensive CI/CD Pipeline Analytics & Monitoring</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tab layout with sync button
    tab_col, sync_col = st.columns([0.95, 0.05])
    
    with tab_col:
        # Use tabs for main navigation with enhanced styling
        main_tab1, main_tab2, main_tab3 = st.tabs([
            "📊 Overview", 
            "🧹 Cleanup Insights", 
            "📈 Analytics"
        ])
    
    with sync_col:
        # Data sync button - small and subtle
        sync_clicked = st.button("🔄", key="data_sync", help="Sync Data from Jenkins", use_container_width=True)
        if sync_clicked:
            st.session_state.show_sync_modal = True
            st.rerun()
    
    # Data sync modal appears below the tabs (full width)
    if st.session_state.get('show_sync_modal', False):
        st.markdown("---")
        st.markdown("### 🔄 Data Synchronization")
        
        # Show current data status
        if hasattr(st.session_state, 'jobs_count') and hasattr(st.session_state, 'last_sync_time'):
            st.info(f"📊 **Current Data**: {st.session_state.jobs_count} jobs loaded • Last updated: {st.session_state.last_sync_time}")
        
        # Warning message
        st.warning("⚠️ **Data Sync Warning**: This will fetch fresh data from Jenkins and may take some time. Only use when you need the latest information.")
        
        # Confirmation checkbox
        sync_confirmed = st.checkbox("I understand and want to sync data from Jenkins")
        
        # Sync button (only enabled if confirmed)
        refresh_button = st.button(
            "🔄 Sync Latest Data from Jenkins", 
            disabled=not sync_confirmed,
            use_container_width=True
        )
        
        if refresh_button:
            st.info("🔄 Syncing data from Jenkins...")
            # Trigger data refresh by setting session state
            st.session_state.refresh_data = True
            st.session_state.show_sync_modal = False
            st.rerun()
        
        # Close button
        if st.button("❌ Close", use_container_width=True):
            st.session_state.show_sync_modal = False
            st.rerun()
        
        st.markdown("---")
    
    with main_tab1:
        render_dashboard_tab(df)
    
    with main_tab2:
        render_cleanup_tab(df)
    
    with main_tab3:
        render_analytics_tab(df)


def render_dashboard_tab(df):
    """Render the main dashboard with modern styling and enhanced visualizations"""
    
    # Define total_items at the beginning
    total_items = len(df)
    
    # Horizontal Filter Bar - moved from sidebar to main content
    st.markdown("""
    <div class="section-header">
        <h2>🔍 Search & Filters</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Filter controls in horizontal layout - adjusted widths for better folder names
    col1, col2, col3 = st.columns([1.5, 2, 1])
    
    with col1:
        # Smart search with autocomplete suggestions
        search_term = st.text_input(
            "🔎 Quick Search",
            placeholder="Search by job name, folder, or status...",
            help="Type to search across all fields"
        )
    
    with col2:
        # Simple dropdown for folder filter
        unique_folders = sorted(df["folder"].unique())
        folder_filter_multiselect = st.multiselect(
            "📁 Folders",
            options=unique_folders,
            default=[],  # No default selection - show all folders
            help="Select specific folders to include (leave empty to show all)"
        )
    
    with col3:
        # Simple dropdown for status filter
        unique_statuses = sorted(df["last_build_status"].unique())
        status_filter_multiselect = st.multiselect(
            "🎯 Status",
            options=unique_statuses,
            default=[],  # No default selection - show all statuses
            help="Select specific statuses to include (leave empty to show all)"
        )
    
    # Advanced search options in an expander
    with st.expander("🔧 Advanced Search Options", expanded=False):
        adv_col1, adv_col2, adv_col3 = st.columns(3)
        with adv_col1:
            name_filter = st.text_input("Filter by Name (exact match)")
        with adv_col2:
            folder_filter = st.text_input("Filter by Folder (exact match)")
        with adv_col3:
            status_filter = st.selectbox("Filter by Status", ["All"] + sorted(df["last_build_status"].unique().tolist()))
    
    # Apply filters
    filtered_df = apply_filters(df, search_term, name_filter, folder_filter, status_filter, 
                               folder_filter_multiselect, status_filter_multiselect, [])
    
    # Enhanced visualizations with modern styling (showing filtered data)
    render_enhanced_visualizations(filtered_df, len(filtered_df), total_items)
    
    # Enhanced data display with integrated pagination
    render_enhanced_data_table(filtered_df, len(filtered_df))


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
    """Render enhanced visualizations with modern styling and better charts"""
    if not df.empty:
        # Simple header without card
        st.markdown("""
        <div class="section-header">
            <h2>🎯 Key Performance Indicators</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # KPI Cards with equal size and center alignment
        col1, col2, col3, col4 = st.columns(4)
        
        # Custom CSS for equal-sized KPI cards
        st.markdown("""
        <style>
        .stMetric {
            text-align: center !important;
            height: 120px !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: center !important;
            align-items: center !important;
        }
        .stMetric > div {
            text-align: center !important;
        }
        .stMetric label {
            text-align: center !important;
            justify-content: center !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        with col1:
            success_count = len(df[df["last_build_status"] == "SUCCESS"])
            success_rate = (success_count / len(df)) * 100 if len(df) > 0 else 0
            st.metric(
                "✅ Success Rate", 
                f"{success_rate:.1f}%", 
                f"{success_count} jobs",
                delta_color="normal"
            )
        
        with col2:
            failure_count = len(df[df["last_build_status"] == "FAILURE"])
            failure_rate = (failure_count / len(df)) * 100 if len(df) > 0 else 0
            st.metric(
                "❌ Failure Rate", 
                f"{failure_rate:.1f}%", 
                f"{failure_count} jobs",
                delta_color="inverse"
            )
        
        with col3:
            inactive_count = len(df[df["days_since_last_build"] > DashboardConfig.INACTIVE_JOB_THRESHOLD_DAYS]) if "days_since_last_build" in df.columns else 0
            st.metric(
                "⏰ Inactive Jobs", 
                inactive_count, 
                f">{DashboardConfig.INACTIVE_JOB_THRESHOLD_DAYS} days",
                delta_color="normal"
            )
        
        with col4:
            # Dynamic Total Jobs card - shows filtered vs total
            if total_filtered_items == total_items:
                # No filters applied - show total jobs
                st.metric(
                    "📊 Total Jobs", 
                    total_items,
                    "All jobs",
                    delta_color="normal"
                )
            else:
                # Filters applied - show filtered/total format
                st.metric(
                    "📊 Total Jobs", 
                    f"{total_filtered_items}/{total_items}",
                    "Filtered jobs",
                    delta_color="normal"
                )
        

        
        # Enhanced pie chart with modern styling
        st.markdown("""
        <div class="section-header">
            <h2>📈 Build Status Distribution</h2>
        </div>
        """, unsafe_allow_html=True)
        
        status_counts = df["last_build_status"].value_counts()
        
        # Create enhanced pie chart with custom colors
        fig = go.Figure(data=[go.Pie(
            labels=status_counts.index,
            values=status_counts.values,
            hole=0.4,
            marker_colors=['#059669', '#dc2626', '#d97706', '#3b82f6', '#8b5cf6'],
            textinfo='label+percent',
            textfont_size=14,
            hoverinfo='label+value+percent'
        )])
        
        fig.update_layout(
            title="Build Status Distribution",
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            height=400,
            margin=dict(t=50, b=50, l=50, r=50)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Enhanced build status trend analysis
        st.markdown("""
        <div class="section-header">
            <h2>📈 Build Status Analysis</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Calculate build status distribution with percentages
        status_counts = df["last_build_status"].value_counts()
        total_jobs = len(df)
        status_percentages = (status_counts / total_jobs * 100).round(1)
        
        # Create a more informative status chart
        fig = go.Figure(data=[go.Bar(
            x=status_counts.index,
            y=status_counts.values,
            text=[f"{count}<br>({pct}%)" for count, pct in zip(status_counts.values, status_percentages)],
            textposition='auto',
            marker_color=['#10b981', '#ef4444', '#f59e0b', '#8b5cf6', '#06b6d4'],
            marker_line_color='rgba(0,0,0,0.1)',
            marker_line_width=1,
            opacity=0.8
        )])
        
        fig.update_layout(
            title="Build Status Distribution with Percentages",
            xaxis_title="Build Status",
            yaxis_title="Number of Jobs",
            height=400,
            margin=dict(t=50, b=50, l=50, r=50),
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data matches the current filters.")


def render_enhanced_data_table(df, total_filtered_items):
    """Render enhanced data table with modern styling and integrated pagination"""
    # Enhanced pagination controls with modern styling
    total_pages = (total_filtered_items + DashboardConfig.ITEMS_PER_PAGE_DEFAULT - 1) // DashboardConfig.ITEMS_PER_PAGE_DEFAULT
    
    if total_pages > 1:
        current_page = 1
    else:
        current_page = 1
    
    start_idx = (current_page - 1) * DashboardConfig.ITEMS_PER_PAGE_DEFAULT
    end_idx = start_idx + DashboardConfig.ITEMS_PER_PAGE_DEFAULT
    paginated_df = df.iloc[start_idx:end_idx]
    
    # Summary info with modern styling
    start_item = (current_page - 1) * DashboardConfig.ITEMS_PER_PAGE_DEFAULT + 1
    end_item = min(current_page * DashboardConfig.ITEMS_PER_PAGE_DEFAULT, total_filtered_items)
    
    if not paginated_df.empty:
        # Enhanced dataframe with modern styling
        st.markdown("""
        <div class="section-header">
            <h2>📊 Jobs Data</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Items per page and page controls side by side
        col1, col2, col3, col4 = st.columns([0.2, 0.15, 0.1, 0.55])
        with col1:
            items_per_page = st.selectbox("📄 Items per page", [25, 50, 100, 200], 
                                        index=[25, 50, 100, 200].index(DashboardConfig.ITEMS_PER_PAGE_DEFAULT))
        
        # Page changing controls (only show if multiple pages)
        if total_pages > 1:
            with col2:
                current_page = st.selectbox(f"📄 Page", range(1, total_pages + 1), index=0)
            with col3:
                st.write(f"of {total_pages}")
            with col4:
                st.write("")  # Empty space for balance
        else:
            with col2:
                st.write("")  # Empty space when no pagination needed
            with col3:
                st.write("")
            with col4:
                st.write("")
        
        # Recalculate pagination after page selection
        start_idx = (current_page - 1) * items_per_page
        end_idx = start_idx + items_per_page
        paginated_df = df.iloc[start_idx:end_idx]
        start_item = (current_page - 1) * items_per_page + 1
        end_item = min(current_page * items_per_page, total_filtered_items)
        
        st.info(f"Showing {start_item}-{end_item} of {total_filtered_items} jobs")
        
        # Select only the columns we want to display
        display_columns = [
            "name", "folder", "last_build_status", "success_rate",
            "days_since_last_build", "total_builds", "url"
        ]
        
        # Filter dataframe to only show selected columns
        display_df = paginated_df[display_columns].copy()
        
        # Enhanced dataframe with cleaner columns and modern styling
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
    """Render the cleanup insights tab with modern styling and enhanced organization"""
    # Create sub-tabs with modern styling
    cleanup_tab1, cleanup_tab2, cleanup_tab3, cleanup_tab4 = st.tabs([
        "📊 Summary", 
        "🧪 Test Jobs", 
        "⏰ Inactive Jobs", 
        "🚫 Disabled Jobs"
    ])
    
    with cleanup_tab1:
        render_cleanup_summary(df)
    
    with cleanup_tab2:
        render_test_jobs_section(df)
    
    with cleanup_tab3:
        render_inactive_jobs_section(df)
    
    with cleanup_tab4:
        render_disabled_jobs_section(df)


def render_test_jobs_section(df):
    st.markdown("""
    <div class="section-header">
        <h2>🧪 Test Jobs</h2>
        <p>Jobs that appear to be test/demo/temporary pipelines</p>
    </div>
    """, unsafe_allow_html=True)
    
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
    st.markdown(f"""
    <div class="section-header">
        <h2>⏰ Inactive Jobs</h2>
        <p>Jobs that haven't been triggered for {DashboardConfig.INACTIVE_JOB_THRESHOLD_DAYS}+ days</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Filter for jobs with last build more than threshold days ago
    inactive_jobs = df[
        (df["days_since_last_build"] > DashboardConfig.INACTIVE_JOB_THRESHOLD_DAYS) & 
        (df["days_since_last_build"].notna())
    ].copy()
    
    if not inactive_jobs.empty:
        st.info(f"Found {len(inactive_jobs)} inactive jobs")
        
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
    st.markdown("""
    <div class="section-header">
        <h2>🚫 Disabled Jobs</h2>
        <p>Jobs that are currently disabled</p>
    </div>
    """, unsafe_allow_html=True)
    
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
    """Render cleanup summary with modern styling and enhanced insights"""
    
    # Calculate cleanup metrics
    test_jobs = df[df["is_test_job"] == True]
    inactive_jobs = df[df["days_since_last_build"] > DashboardConfig.INACTIVE_JOB_THRESHOLD_DAYS] if "days_since_last_build" in df.columns else pd.DataFrame()
    disabled_jobs = df[df["is_disabled"] == True] if "is_disabled" in df.columns else pd.DataFrame()
    
    # Enhanced KPI cards for cleanup summary
    st.markdown("""
    <div class="section-header">
        <h2>🎯 Cleanup Metrics</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Custom CSS for equal-sized KPI cards
    st.markdown("""
    <style>
    .stMetric {
        text-align: center !important;
        height: 120px !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
    }
    .stMetric > div {
        text-align: center !important;
    }
    .stMetric label {
        text-align: center !important;
        justify-content: center !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "🧪 Test Jobs", 
            len(test_jobs),
            f"{len(test_jobs)/len(df)*100:.1f}% of total",
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            "⏰ Inactive Jobs", 
            len(inactive_jobs),
            f">{DashboardConfig.INACTIVE_JOB_THRESHOLD_DAYS} days old",
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            "🚫 Disabled Jobs", 
            len(disabled_jobs),
            f"{len(disabled_jobs)/len(df)*100:.1f}% of total",
            delta_color="inverse"
        )
    
    with col4:
        total_cleanup_candidates = len(test_jobs) + len(inactive_jobs) + len(disabled_jobs)
        st.metric(
            "📋 Total Candidates", 
            total_cleanup_candidates,
            f"{total_cleanup_candidates/len(df)*100:.1f}% of total",
            delta_color="inverse"
        )
    
    # Cleanup recommendations with modern styling
    st.markdown("""
    <div class="section-header">
        <h2>💡 Cleanup Recommendations</h2>
    </div>
    """, unsafe_allow_html=True)
    
    recommendations = []
    
    if len(test_jobs) > len(df) * 0.1:
        recommendations.append("⚠️ **High number of test jobs** - Consider reviewing and removing outdated test jobs")
    elif len(test_jobs) > 0:
        recommendations.append("✅ **Test jobs under control** - Current test job count is manageable")
    
    if len(inactive_jobs) > len(df) * 0.2:
        recommendations.append("⚠️ **Many inactive jobs** - Consider archiving or removing jobs inactive for >60 days")
    elif len(inactive_jobs) > 0:
        recommendations.append("✅ **Inactive jobs manageable** - Consider reviewing long-inactive jobs")
    
    if len(disabled_jobs) > len(df) * 0.05:
        recommendations.append("⚠️ **Several disabled jobs** - Review disabled jobs and remove if no longer needed")
    elif len(disabled_jobs) > 0:
        recommendations.append("✅ **Disabled jobs under control** - Current disabled job count is acceptable")
    
    if not recommendations:
        recommendations.append("🎉 **Excellent pipeline hygiene!** - Your Jenkins instance is well-maintained")
    
    for rec in recommendations:
        st.markdown(f"• {rec}")
    
    # Cleanup progress visualization
    st.markdown("""
    <div class="section-header">
        <h2>📊 Cleanup Progress</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Create cleanup progress chart
    categories = ['Test Jobs', 'Inactive Jobs', 'Disabled Jobs', 'Active Jobs']
    values = [len(test_jobs), len(inactive_jobs), len(disabled_jobs), 
              len(df) - len(test_jobs) - len(inactive_jobs) - len(disabled_jobs)]
    colors = ['#f59e0b', '#ef4444', '#8b5cf6', '#10b981']
    
    fig = go.Figure(data=[go.Bar(
        x=categories,
        y=values,
        marker_color=colors,
        marker_line_color='rgba(0,0,0,0.1)',
        marker_line_width=1,
        opacity=0.8
    )])
    
    fig.update_layout(
        title="Job Distribution by Cleanup Category",
        xaxis_title="Job Category",
        yaxis_title="Number of Jobs",
        height=400,
        margin=dict(t=50, b=50, l=50, r=50),
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)


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


def render_analytics_tab(df):
    """Render the Analytics tab with modern styling and enhanced visualizations"""
    # Filter out jobs without duration data
    jobs_with_duration = df[df["avg_build_duration"] > 0].copy()
    
    if jobs_with_duration.empty:
        st.warning("No build duration data available. Please refresh the data to see analytics.")
        return
    
    # Convert duration from milliseconds to minutes for better readability
    jobs_with_duration["avg_build_duration_min"] = jobs_with_duration["avg_build_duration"] / 60000
    jobs_with_duration["last_build_duration_min"] = jobs_with_duration["last_build_duration"] / 60000
    jobs_with_duration["avg_successful_duration_min"] = jobs_with_duration["avg_successful_duration"] / 60000
    jobs_with_duration["avg_failed_duration_min"] = jobs_with_duration["avg_failed_duration"] / 60000
    
    # Create sub-tabs with modern styling
    analytics_tab1, analytics_tab2, analytics_tab3 = st.tabs([
        "⏱️ Build Duration Analysis", 
        "📊 Performance Insights",
        "🔍 Outlier Analysis"
    ])
    
    with analytics_tab1:
        render_build_duration_analysis(jobs_with_duration)
    
    with analytics_tab2:
        render_performance_insights(jobs_with_duration)
    
    with analytics_tab3:
        render_outlier_analysis(jobs_with_duration, jobs_with_duration)


def render_build_duration_analysis(df):
    """Render build duration analysis with modern styling and enhanced charts"""
    
    # Data cleaning: Remove unrealistic values (more than 24 hours = 1440 minutes)
    df_clean = df[df["avg_build_duration_min"] <= 1440].copy()
    
    if len(df_clean) < len(df):
        df = df_clean
    
    # Duration statistics with modern styling
    st.markdown("""
    <div class="section-header">
        <h2>📊 Duration Statistics</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_duration = df["avg_build_duration_min"].mean()
        st.metric("Average Build Duration", f"{avg_duration:.1f} min")
    
    with col2:
        median_duration = df["avg_build_duration_min"].median()
        st.metric("Median Build Duration", f"{median_duration:.1f} min")
    
    with col3:
        max_duration = df["avg_build_duration_min"].max()
        if max_duration > 60:
            # Format as hours if more than 60 minutes
            max_duration_hrs = max_duration / 60
            st.metric("Longest Average Build", f"{max_duration_hrs:.1f} hours")
        else:
            st.metric("Longest Average Build", f"{max_duration:.1f} min")
    
    with col4:
        total_build_time = df["total_build_duration"].sum() / 60000 / 60  # Convert to hours
        st.metric("Total Build Time", f"{total_build_time:.1f} hours")
    
    # Duration distribution chart with modern styling
    st.markdown("""
    <div class="section-header">
        <h2>📊 Build Duration Distribution</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Create duration bins
    df["duration_bin"] = pd.cut(df["avg_build_duration_min"], 
                               bins=[0, 5, 15, 30, 60, 120, float('inf')],
                               labels=["0-5 min", "5-15 min", "15-30 min", "30-60 min", "1-2 hours", "2+ hours"])
    
    duration_dist = df["duration_bin"].value_counts().sort_index()
    
    fig = go.Figure(data=[go.Bar(
        x=duration_dist.index,
        y=duration_dist.values,
        marker_color='#6366f1',
        marker_line_color='#4f46e5',
        marker_line_width=1,
        opacity=0.8
    )])
    
    fig.update_layout(
        title="Distribution of Average Build Durations",
        xaxis_title="Duration Range",
        yaxis_title="Number of Jobs",
        height=400,
        margin=dict(t=50, b=50, l=50, r=50),
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Duration vs Success Rate scatter plot with modern styling
    st.markdown("""
    <div class="section-header">
        <h2>📈 Duration vs Success Rate Correlation</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Create color mapping for status
    color_map = {
        'SUCCESS': '#10b981',
        'FAILURE': '#ef4444',
        'UNSTABLE': '#f59e0b',
        'ABORTED': '#8b5cf6',
        'IN_PROGRESS': '#06b6d4'
    }
    
    fig = go.Figure()
    
    for status in df['last_build_status'].unique():
        status_data = df[df['last_build_status'] == status]
        fig.add_trace(go.Scatter(
            x=status_data["avg_build_duration_min"],
            y=status_data["success_rate"],
            mode='markers',
            name=status,
            marker=dict(
                color=color_map.get(status, '#6366f1'),
                size=8,
                opacity=0.7
            ),
            hovertemplate='<b>%{text}</b><br>' +
                         'Duration: %{x:.1f} min<br>' +
                         'Success Rate: %{y:.1f}%<br>' +
                         'Status: ' + status +
                         '<extra></extra>',
            text=status_data['name']
        ))
    
    fig.update_layout(
        title="Build Duration vs Success Rate",
        xaxis_title="Average Build Duration (minutes)",
        yaxis_title="Success Rate (%)",
        height=500,
        margin=dict(t=50, b=50, l=50, r=50),
        hovermode='closest'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Longest builds table with modern styling
    st.markdown("""
    <div class="section-header">
        <h2>🐌 Longest Running Jobs</h2>
    </div>
    """, unsafe_allow_html=True)
    
    longest_jobs = df.nlargest(10, "avg_build_duration_min")[["name", "folder", "avg_build_duration_min", "success_rate", "total_builds"]]
    
    st.dataframe(
        longest_jobs,
        column_config={
            "avg_build_duration_min": st.column_config.NumberColumn("Avg Duration (min)", format="%.1f"),
            "success_rate": st.column_config.NumberColumn("Success Rate (%)", format="%.1f"),
            "total_builds": st.column_config.NumberColumn("Total Builds", format="%d"),
        },
        use_container_width=True
    )


def render_outlier_analysis(df_clean, df_original):
    """Render outlier analysis with explanations and recommendations"""
    st.markdown("""
    <div class="section-header">
        <h2>🔍 Outlier Analysis</h2>
        <p>Jobs with unusual characteristics that may need attention</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Find outliers (jobs with unrealistic build durations)
    outliers = df_clean[df_clean["avg_build_duration_min"] > 1440].copy()
    
    if not outliers.empty:
        st.warning(f"⚠️ Found {len(outliers)} jobs with unrealistic build durations (>24 hours)")
        
        # Add analysis and recommendations
        outliers["outlier_type"] = outliers.apply(analyze_outlier_reason, axis=1)
        outliers["recommendation"] = outliers.apply(get_outlier_recommendation, axis=1)
        
        # Display outliers table
        st.markdown("""
        <div class="section-header">
            <h2>🐌 Unusually Long Build Jobs</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.dataframe(
            outliers[["name", "folder", "avg_build_duration_min", "last_build_status", "total_builds", "outlier_type", "recommendation", "url"]],
            column_config={
                "url": st.column_config.LinkColumn("🔗 Job URL"),
                "avg_build_duration_min": st.column_config.NumberColumn("Avg Duration (hrs)", format="%.1f"),
                "total_builds": st.column_config.NumberColumn("Total Builds", format="%d"),
            },
            use_container_width=True
        )
        
        # Summary insights
        st.markdown("""
        <div class="section-header">
            <h2>💡 Outlier Insights</h2>
        </div>
        """, unsafe_allow_html=True)
        
        outlier_types = outliers["outlier_type"].value_counts()
        for outlier_type, count in outlier_types.items():
            st.info(f"**{outlier_type}**: {count} jobs")
            
    else:
        st.success("🎉 No outliers found! All jobs have realistic build durations.")


def analyze_outlier_reason(row):
    """Analyze why a job might be an outlier"""
    duration_hrs = row["avg_build_duration_min"] / 60
    
    if duration_hrs > 168:  # More than 1 week
        return "🚨 Extremely Long Build (>1 week)"
    elif duration_hrs > 72:  # More than 3 days
        return "⚠️ Very Long Build (3+ days)"
    elif duration_hrs > 48:  # More than 2 days
        return "🐌 Long Build (2+ days)"
    elif duration_hrs > 24:  # More than 1 day
        return "⏰ Extended Build (1+ day)"
    else:
        return "📊 Unusual Build Duration"


def get_outlier_recommendation(row):
    """Get recommendation for outlier job"""
    duration_hrs = row["avg_build_duration_min"] / 60
    
    if duration_hrs > 168:
        return "🔧 Investigate immediately - likely stuck or misconfigured"
    elif duration_hrs > 72:
        return "📋 Review build process - consider optimization or parallelization"
    elif duration_hrs > 48:
        return "👀 Monitor closely - may need process improvements"
    elif duration_hrs > 24:
        return "📊 Analyze build steps - look for optimization opportunities"
    else:
        return "🔍 Review build configuration"


def render_performance_insights(df):
    """Render performance insights with modern styling and enhanced visualizations"""
    # Data cleaning: Remove unrealistic values (more than 24 hours = 1440 minutes)
    df_clean = df[df["avg_build_duration_min"] <= 1440].copy()
    if len(df_clean) < len(df):
        df = df_clean
    
    # Calculate insights
    total_jobs = len(df)
    avg_duration = df["avg_build_duration_min"].mean()
    median_duration = df["avg_build_duration_min"].median()
    max_duration = df["avg_build_duration_min"].max()
    
    # KPI Cards with modern styling
    st.markdown("""
    <div class="section-header">
        <h2>📈 Key Metrics</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Custom CSS for equal-sized KPI cards
    st.markdown("""
    <style>
    .stMetric {
        text-align: center !important;
        height: 120px !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
    }
    .stMetric > div {
        text-align: center !important;
    }
    .stMetric label {
        text-align: center !important;
        justify-content: center !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Average Build Duration", f"{avg_duration:.1f} min")
    
    with col2:
        st.metric("Median Build Duration", f"{median_duration:.1f} min")
    
    with col3:
        st.metric("Longest Average Build", f"{max_duration:.1f} min")
    
    with col4:
        total_build_time = df["total_build_duration"].sum() / 60000 / 60  # Convert to hours
        st.metric("Total Build Time", f"{total_build_time:.1f} hours")
    
    # Performance insights with modern styling
    st.markdown("""
    <div class="section-header">
        <h2>🎯 Performance Insights</h2>
    </div>
    """, unsafe_allow_html=True)
    
    insights = []
    
    if avg_duration > 30:
        insights.append("⚠️ **Average build duration is high** - Consider optimizing build processes or parallelization")
    elif avg_duration < 10:
        insights.append("💡 **Average build duration is low** - This might indicate efficient builds")
    
    if median_duration > 30:
        insights.append("⚠️ **Median build duration is high** - This could indicate a slow-moving pipeline or a bottleneck")
    elif median_duration < 10:
        insights.append("💡 **Median build duration is low** - This might be a sign of efficient builds")
    
    if max_duration > 60:
        insights.append("⚠️ **Longest average build is high** - This could indicate a slow-moving pipeline or a bottleneck")
    elif max_duration < 10:
        insights.append("💡 **Longest average build is low** - This might be a sign of efficient builds")
    
    if total_build_time > 100:
        insights.append("⚠️ **Total build time is high** - Consider optimizing build processes or parallelization")
    elif total_build_time < 50:
        insights.append("💡 **Total build time is low** - This might indicate efficient builds")
    
    if not insights:
        insights.append("🎉 **Great performance!** - Your Jenkins instance is well-optimized")
    
    for insight in insights:
        st.markdown(f"• {insight}")
    
    # Folder analysis with modern styling
    st.markdown("""
    <div class="section-header">
        <h2>📁 Performance by Folder</h2>
    </div>
    """, unsafe_allow_html=True)
    
    folder_performance = df.groupby("folder").agg({
        "avg_build_duration_min": "mean",
        "success_rate": "mean",
        "name": "count"
    }).rename(columns={"name": "job_count"})
    
    # Only show folders with multiple jobs
    folder_performance = folder_performance[folder_performance["job_count"] >= 3].sort_values("avg_build_duration_min", ascending=False)
    
    if not folder_performance.empty:
        fig = go.Figure(data=[go.Bar(
            x=folder_performance.index,
            y=folder_performance["avg_build_duration_min"],
            marker_color='#8b5cf6',
            marker_line_color='#7c3aed',
            marker_line_width=1,
            opacity=0.8
        )])
        
        fig.update_layout(
            title="Average Build Duration by Folder",
            xaxis_title="Folder",
            yaxis_title="Duration (minutes)",
            height=400,
            margin=dict(t=50, b=50, l=50, r=50),
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show folder details with modern styling
        st.markdown("""
        <div class="section-header">
            <h2>📊 Folder Details</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.dataframe(
            folder_performance,
            column_config={
                "avg_build_duration_min": st.column_config.NumberColumn("Avg Duration (min)", format="%.1f"),
                "success_rate": st.column_config.NumberColumn("Success Rate (%)", format="%.1f"),
                "job_count": st.column_config.NumberColumn("Job Count", format="%d"),
            },
            use_container_width=True
        )
