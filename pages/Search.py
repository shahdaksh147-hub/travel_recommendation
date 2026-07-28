"""
pages/Search.py
================
Renders the Search page: lets users find destinations by name and/or
category, and browse the matching results.
"""

import streamlit as st
from utils.preprocessing import load_destinations


@st.cache_data
def _load_data():
    """Load and cache the destinations dataset."""
    return load_destinations()


def render() -> None:
    """Render the Search page UI and filtered results."""
    st.title("🔍 Search Destinations")
    st.caption("Find a destination by name, or browse by category.")
    st.write("")

    df = _load_data()
    categories = ["All Categories"] + sorted(df["Category"].unique())

    col1, col2 = st.columns([2, 1])
    with col1:
        query = st.text_input("Search by destination name", placeholder="e.g. Goa, Kyoto, Rishikesh")
    with col2:
        category = st.selectbox("Filter by category", categories)

    filtered = _apply_filters(df, query, category)

    st.write(f"**{len(filtered)}** destination(s) found.")
    st.write("")

    if filtered.empty:
        st.info("No destinations match your search. Try a different name or category.")
        return

    _render_results(filtered)


def _apply_filters(df, query: str, category: str):
    """
    Filter the dataset by name substring and/or category.

    Args:
        df: The full destinations DataFrame.
        query: Free-text search string for the destination name.
        category: Selected category, or "All Categories" for no filter.

    Returns:
        A filtered DataFrame, sorted by rating (highest first).
    """
    filtered = df.copy()

    if query:
        filtered = filtered[filtered["Destination_Name"].str.contains(query, case=False, na=False)]

    if category != "All Categories":
        filtered = filtered[filtered["Category"] == category]

    return filtered.sort_values("Rating", ascending=False)


def _render_results(filtered) -> None:
    """
    Render each matching destination as an expandable card.

    Args:
        filtered: The filtered/sorted DataFrame to display.
    """
    for _, row in filtered.iterrows():
        header = f"{row['Destination_Name']} — {row['State']}, {row['Country']} ({row['Category']})"
        with st.expander(header):
            st.write(row["Description"])

            c1, c2, c3 = st.columns(3)
            c1.metric("Budget / Day", f"${row['Budget']:,}")
            c2.metric("Rating", f"{row['Rating']} ★")
            c3.metric("Best Season", row["Best_Season"])
