import streamlit as st

from utils.preprocessing import load_destinations


def render():

    st.title("🔍 Search Destinations")

    df = load_destinations()

    query = st.text_input(
        "Search Destination"
    )

    category = st.selectbox(

        "Category",

        ["All"]

        + sorted(df["Category"].unique())

    )

    results = df.copy()

    if query:

        results = results[

            results["Destination_Name"]

            .str.contains(

                query,

                case=False,

                na=False,

            )

        ]

    if category != "All":

        results = results[

            results["Category"]

            == category

        ]

    st.write(
        f"Found **{len(results)}** destination(s)"
    )

    st.dataframe(

        results[

            [

                "Destination_Name",

                "Country",

                "Category",

                "Budget",

                "Rating",

            ]

        ],

        use_container_width=True,

    )
