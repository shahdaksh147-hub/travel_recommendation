"""
pages/Dashboard.py
===================
Renders the Dashboard page: summary metrics and interactive charts
describing the destinations dataset as a whole (not personalized to
any single user's preferences).
"""

import streamlit as st
import pandas as pd
import plotly.express as px

from utils.preprocessing import load_destinations, DataPreprocessor


@st.cache_data
def _load_data():
    """Load and cache the destinations dataset."""
    return load_destinations()


def render() -> None:
    """Render the Dashboard page UI."""
    st.title("📊 Dashboard")
    st.caption("Trends and stats across the entire destination catalog.")
    st.write("")

    df = _load_data()
    stats = DataPreprocessor().get_dashboard_stats(df)

    _render_summary_metrics(stats)
    st.write("")
    _render_charts(stats)


def _render_summary_metrics(stats: dict) -> None:
    """Render the top-level summary metrics row."""
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Destinations", stats["total_destinations"])
    col2.metric("Total Categories", stats["total_categories"])
    col3.metric("Average Rating", f"{stats['average_rating']} ★")


def _render_charts(stats: dict) -> None:
    """Render the category and budget distribution charts side by side."""
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader("Category Distribution")
        category_df = (
            pd.DataFrame(list(stats["category_counts"].items()), columns=["Category", "Count"])
            .sort_values("Count", ascending=False)
        )
        fig = px.bar(
            category_df, x="Category", y="Count", color="Category", text="Count",
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with chart_col2:
        st.subheader("Budget Distribution")
        budget_df = pd.DataFrame(list(stats["budget_distribution"].items()), columns=["Range", "Count"])
        fig2 = px.pie(budget_df, names="Range", values="Count", hole=0.45)
        st.plotly_chart(fig2, use_container_width=True)
