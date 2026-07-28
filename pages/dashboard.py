import streamlit as st
import plotly.express as px

from utils.preprocessing import (
    load_destinations,
    DataPreprocessor,
)


def render():

    st.title("📊 Dashboard")

    df = load_destinations()

    stats = DataPreprocessor().dashboard_stats(df)

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Destinations",
        stats["total_destinations"]
    )

    c2.metric(
        "Categories",
        stats["categories"]
    )

    c3.metric(
        "Average Rating",
        stats["average_rating"]
    )

    st.divider()

    chart1 = px.bar(

        x=list(stats["category_counts"].keys()),

        y=list(stats["category_counts"].values()),

        title="Category Distribution"

    )

    st.plotly_chart(
        chart1,
        use_container_width=True
    )

    chart2 = px.pie(

        names=list(stats["budget_distribution"].keys()),

        values=list(stats["budget_distribution"].values()),

        title="Budget Distribution"

    )

    st.plotly_chart(
        chart2,
        use_container_width=True
    )
