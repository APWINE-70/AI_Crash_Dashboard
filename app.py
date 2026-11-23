"""
AI Crash & Incident Dashboard
A real-time monitoring and analytics dashboard for AI/ML model crashes,
latency spikes, hallucinations, and infrastructure failures.
"""

from datetime import datetime, timedelta
import random
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Configure page settings
st.set_page_config(
    page_title="AI Crash & Incident Dashboard",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Generate sample incident data for demonstration
@st.cache_data
def load_incident_data():
    np.random.seed(42)
    models = ["GPT-4o", "Claude-3.5-Sonnet", "Gemini-1.5-Pro", "Llama-3-70B", "Mistral-Large"]
    incident_types = [
        "OOM / GPU Memory Leak",
        "API Rate Limit (429)",
        "Inference Timeout (>30s)",
        "Hallucination / Guardrail Breach",
        "Connection Reset / Host Drop",
        "Token Context Overflow",
    ]
    severities = ["Critical", "High", "Medium", "Low"]
    severity_weights = [0.10, 0.25, 0.40, 0.25]

    data = []
    base_time = datetime.now() - timedelta(days=14)

    for i in range(160):
        timestamp = base_time + timedelta(
            minutes=int(np.random.exponential(scale=120) * (i + 1) % (14 * 24 * 60))
        )
        model = random.choice(models)
        inc_type = random.choice(incident_types)
        severity = np.random.choice(severities, p=severity_weights)
        recovery_time_min = round(random.uniform(2.5, 45.0), 1)

        data.append(
            {
                "Incident ID": f"INC-{1000 + i}",
                "Timestamp": timestamp,
                "Model": model,
                "Incident Type": inc_type,
                "Severity": severity,
                "Recovery Time (min)": recovery_time_min,
                "Status": random.choice(["Resolved", "Resolved", "Resolved", "Investigating"]),
            }
        )

    df = pd.DataFrame(data)
    df = df.sort_values(by="Timestamp", ascending=False).reset_index(drop=True)
    return df


# Main application
def main():
    # Sidebar
    st.sidebar.title("🚨 Controls & Filters")
    st.sidebar.markdown("Filter and drill down into AI incidents.")

    df = load_incident_data()

    # Filter: Model Selection
    all_models = list(df["Model"].unique())
    selected_models = st.sidebar.multiselect(
        "Select Model(s)",
        options=all_models,
        default=all_models,
    )

    # Filter: Severity Selection
    all_severities = ["Critical", "High", "Medium", "Low"]
    selected_severities = st.sidebar.multiselect(
        "Incident Severity",
        options=all_severities,
        default=all_severities,
    )

    # Filter: Status Selection
    all_statuses = list(df["Status"].unique())
    selected_statuses = st.sidebar.multiselect(
        "Status",
        options=all_statuses,
        default=all_statuses,
    )

    # Apply filters
    filtered_df = df[
        (df["Model"].isin(selected_models))
        & (df["Severity"].isin(selected_severities))
        & (df["Status"].isin(selected_statuses))
    ]

    # Dashboard Header
    st.title("🚨 AI Crash & Incident Dashboard")
    st.caption("Centralized telemetry and reliability monitoring for production LLMs & AI pipelines.")

    st.markdown("---")

    # High-level KPIs
    col1, col2, col3, col4 = st.columns(4)

    total_incidents = len(filtered_df)
    critical_count = len(filtered_df[filtered_df["Severity"] == "Critical"])
    avg_recovery = (
        round(filtered_df["Recovery Time (min)"].mean(), 1) if total_incidents > 0 else 0.0
    )
    active_incidents = len(filtered_df[filtered_df["Status"] == "Investigating"])

    col1.metric("Total Incidents", total_incidents, delta=f"{len(df)} total logged")
    col2.metric("Critical Crashes", critical_count, delta_color="inverse")
    col3.metric("Avg. Recovery (MTTR)", f"{avg_recovery} m")
    col4.metric("Active / Investigating", active_incidents, delta_color="inverse")

    st.markdown("---")

    # Visualizations
    v_col1, v_col2 = st.columns([3, 2])

    with v_col1:
        st.subheader("📈 Crash Incidents Over Time")
        if not filtered_df.empty:
            timeline_df = (
                filtered_df.set_index("Timestamp")
                .resample("1D")["Incident ID"]
                .count()
                .reset_index(name="Count")
            )
            fig_timeline = px.line(
                timeline_df,
                x="Timestamp",
                y="Count",
                markers=True,
                title="Daily Incident Frequency",
                labels={"Count": "Incident Count", "Timestamp": "Date"},
            )
            fig_timeline.update_layout(template="plotly_white", height=350)
            st.plotly_chart(fig_timeline, use_container_width=True)
        else:
            st.info("No data available for selected filters.")

    with v_col2:
        st.subheader("🎯 Severity Breakdown")
        if not filtered_df.empty:
            color_map = {
                "Critical": "#FF4B4B",
                "High": "#FFAA00",
                "Medium": "#0068C9",
                "Low": "#29B5E8",
            }
            fig_pie = px.pie(
                filtered_df,
                names="Severity",
                title="Proportion by Severity",
                color="Severity",
                color_discrete_map=color_map,
                hole=0.45,
            )
            fig_pie.update_layout(height=350)
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No data available.")

    # Breakdown by Model and Crash Type
    b_col1, b_col2 = st.columns(2)

    with b_col1:
        st.subheader("🤖 Incidents by Model")
        if not filtered_df.empty:
            model_summary = (
                filtered_df.groupby(["Model", "Severity"]).size().reset_index(name="Incidents")
            )
            fig_model = px.bar(
                model_summary,
                x="Model",
                y="Incidents",
                color="Severity",
                barmode="stack",
                title="Incident Volume by Model Architecture",
            )
            fig_model.update_layout(template="plotly_white", height=320)
            st.plotly_chart(fig_model, use_container_width=True)

    with b_col2:
        st.subheader("💥 Top Incident Root Causes")
        if not filtered_df.empty:
            type_counts = (
                filtered_df["Incident Type"]
                .value_counts()
                .reset_index(name="Frequency")
            )
            type_counts.columns = ["Incident Type", "Frequency"]
            fig_causes = px.bar(
                type_counts,
                x="Frequency",
                y="Incident Type",
                orientation="h",
                title="Incident Types Distribution",
                color="Frequency",
                color_continuous_scale="Blues",
            )
            fig_causes.update_layout(template="plotly_white", height=320)
            st.plotly_chart(fig_causes, use_container_width=True)

    # Incident Log Table
    st.markdown("---")
    st.subheader("📋 Incident Telemetry Log")

    # Search bar
    search_query = st.text_input("🔍 Search by Incident ID or keywords", "")
    display_df = filtered_df.copy()
    if search_query:
        display_df = display_df[
            display_df["Incident ID"].str.contains(search_query, case=False, na=False)
            | display_df["Incident Type"].str.contains(search_query, case=False, na=False)
        ]

    st.dataframe(
        display_df,
        use_container_width=True,
        column_config={
            "Timestamp": st.column_config.DatetimeColumn("Timestamp", format="YYYY-MM-DD HH:mm"),
            "Recovery Time (min)": st.column_config.NumberColumn("Recovery (min)", format="%.1f min"),
        },
    )


if __name__ == "__main__":
    main()
