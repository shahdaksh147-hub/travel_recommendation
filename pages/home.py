import streamlit as st

from utils.preprocessing import load_destinations


def render():

    user = st.session_state.get("user", {})

    st.title(f"👋 Welcome {user.get('full_name', 'Traveler')}")

    st.write(
        """
        Welcome to **Wherever Next**.

        Discover amazing travel destinations using our AI-powered recommendation engine.
        """
    )

    st.divider()

    df = load_destinations()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Destinations", len(df))
    c2.metric("Categories", df["Category"].nunique())
    c3.metric("Countries", df["Country"].nunique())
    c4.metric("Average Rating", round(df["Rating"].mean(), 1))

    st.divider()

    st.subheader("Dataset Preview")

    st.dataframe(
        df[
            [
                "Destination_Name",
                "Country",
                "Category",
                "Budget",
                "Rating",
            ]
        ].head(10),
        use_container_width=True,
    )
