"""
pages/Home.py
=============
Renders the Home page: a welcome message for the logged-in user,
a short project overview, a live dataset snapshot, and quick-navigation
cards previewing the app's main features.
"""

import streamlit as st
from utils.preprocessing import load_destinations


@st.cache_data
def _load_data():
    """Load and cache the destinations dataset for the home page snapshot."""
    return load_destinations()


def render() -> None:
    """Render the Home page UI."""
    user = st.session_state.get("user") or {}
    full_name = user.get("full_name", "Traveler")

    st.title(f"👋 Welcome, {full_name}!")
    st.caption("Your AI-powered co-pilot for planning where to go next.")
    st.write("")

    _render_overview()
    st.write("")
    _render_quick_stats()
    st.write("")
    _render_quick_navigation()


def _render_overview() -> None:
    """Render the project overview section."""
    with st.container(border=True):
        st.subheader("What is Wherever Next?")
        st.write(
            "Wherever Next is a content-based travel recommendation system. "
            "Tell it your preferred destination type, travel season, budget, "
            "and trip length, and it scores every destination in our curated "
            "atlas using **TF-IDF text similarity** blended with **numeric "
            "budget matching** — then ranks the best fits for you. "
            "You can also search the full destination catalog directly, or "
            "browse dataset-wide trends on the Dashboard."
        )


def _render_quick_stats() -> None:
    """Render a small live snapshot of the dataset."""
    try:
        df = _load_data()
    except (FileNotFoundError, ValueError) as e:
        st.warning(f"Dataset could not be loaded: {e}")
        return

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Destinations", len(df))
    col2.metric("Categories", df["Category"].nunique())
    col3.metric("Countries", df["Country"].nunique())
    col4.metric("Avg. Rating", f"{df['Rating'].mean():.1f} ★")


def _render_quick_navigation() -> None:
    """Render quick-navigation preview cards for the app's main features."""
    st.subheader("Where would you like to go?")
    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.markdown("### 🧭 Get Recommendations")
            st.write(
                "Answer four quick questions about your ideal trip and get "
                "your top 5 personalized destination matches."
            )
            st.caption("→ Select **Get Recommendations** in the sidebar.")

    with col2:
        with st.container(border=True):
            st.markdown("### 🔍 Search Destinations")
            st.write(
                "Already have somewhere in mind? Search the full catalog by "
                "name or category."
            )
            st.caption("→ Select **Search Destinations** in the sidebar.")

    with col3:
        with st.container(border=True):
            st.markdown("### 📊 Dashboard")
            st.write(
                "Explore dataset-wide trends: category breakdowns, budget "
                "distribution, and overall ratings."
            )
            st.caption("→ Select **Dashboard** in the sidebar.")
