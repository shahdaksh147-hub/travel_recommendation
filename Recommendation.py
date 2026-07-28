"""
pages/Recommendation.py
========================
Renders the Recommendation page: collects user preferences (destination
type, season, budget, trip duration) and displays the top 5 destinations
from the TravelRecommender engine as result cards.
"""

import streamlit as st
from utils.preprocessing import load_destinations
from models.recommender import TravelRecommender


@st.cache_data
def _load_data():
    """Load and cache the destinations dataset."""
    return load_destinations()


@st.cache_resource
def _get_recommender(_df):
    """
    Build and cache the TravelRecommender (fits a TF-IDF vectorizer,
    which is relatively expensive to redo on every rerun).

    The leading underscore on `_df` tells Streamlit not to attempt to
    hash the DataFrame for cache-key purposes — the dataset is static
    for the lifetime of the app session.
    """
    return TravelRecommender(_df)


def render() -> None:
    """Render the Recommendation page UI and handle form submission."""
    st.title("🧭 Get Recommendations")
    st.caption("Tell us how you like to travel, and we'll find your best matches.")
    st.write("")

    df = _load_data()
    recommender = _get_recommender(df)

    categories = sorted(df["Category"].unique())
    seasons = sorted(df["Best_Season"].unique())

    with st.form("recommend_form"):
        col1, col2 = st.columns(2)
        with col1:
            destination_type = st.selectbox("Destination Type", categories)
            season = st.selectbox("Preferred Season", seasons)
        with col2:
            budget = st.number_input(
                "Total Trip Budget (USD)", min_value=50, max_value=50000, value=1000, step=50
            )
            duration = st.number_input(
                "Trip Duration (days)", min_value=1, max_value=90, value=5, step=1
            )

        submitted = st.form_submit_button(
            "Find My Destinations", type="primary", use_container_width=True
        )

    if submitted:
        with st.spinner("Matching you with destinations..."):
            results = recommender.recommend(
                destination_type=destination_type,
                season=season,
                budget=budget,
                trip_duration_days=duration,
                top_n=5,
            )
        st.write("")
        _render_results(results)


def _render_results(results) -> None:
    """
    Render the top-5 recommendation results as cards.

    Args:
        results: A DataFrame returned by TravelRecommender.recommend().
    """
    if results.empty:
        st.info("No matches found. Try adjusting your preferences.")
        return

    st.subheader("Your Top 5 Matches")

    for _, row in results.iterrows():
        with st.container(border=True):
            header_col, score_col = st.columns([3, 1])

            with header_col:
                st.markdown(f"### {row['Destination_Name']}")
                st.caption(f"{row['State']}, {row['Country']}  ·  {row['Category']}")
                st.write(row["Description"])

            with score_col:
                st.metric("Match Score", f"{row['Match_Score']:.0f}%")
                st.write(f"⭐ {row['Rating']} / 5.0")

            detail_col1, detail_col2 = st.columns(2)
            detail_col1.markdown(f"**💰 Estimated Trip Budget:** ${row['Estimated_Budget']:,}")
            detail_col2.markdown(f"**📅 Best Season:** {row['Best_Season']}")
