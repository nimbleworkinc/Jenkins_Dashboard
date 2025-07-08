import streamlit as st
import plotly.express as px


def render_ui(df):
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
