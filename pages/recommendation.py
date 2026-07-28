import streamlit as st

from utils.preprocessing import load_destinations
from models.recommender import TravelRecommender


@st.cache_resource
def load_model():

    df = load_destinations()

    return df, TravelRecommender(df)


def render():

    st.title("🧭 Travel Recommendation")

    df, model = load_model()

    c1, c2 = st.columns(2)

    with c1:

        category = st.selectbox(
            "Destination Type",
            sorted(df["Category"].unique())
        )

        season = st.selectbox(
            "Season",
            sorted(df["Best_Season"].unique())
        )

    with c2:

        budget = st.slider(
            "Budget",
            100,
            10000,
            1000,
        )

        duration = st.slider(
            "Trip Duration (Days)",
            1,
            30,
            5,
        )

    if st.button(
        "Find Recommendations",
        use_container_width=True,
        type="primary",
    ):

        results = model.recommend(
            category,
            season,
            budget,
            duration,
        )

        st.subheader("Top Destinations")

        for _, row in results.iterrows():

            with st.container(border=True):

                st.markdown(
                    f"### {row['Destination_Name']}"
                )

                st.write(
                    f"📍 {row['State']}, {row['Country']}"
                )

                st.write(
                    row["Description"]
                )

                a, b, c = st.columns(3)

                a.metric(
                    "Rating",
                    row["Rating"]
                )

                b.metric(
                    "Match",
                    f"{row['Match Score']}%"
                )

                c.metric(
                    "Estimated Budget",
                    f"${row['Estimated Budget']:,}"
                )
