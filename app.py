"""
app.py
======
Main entry point for the Wherever Next Travel Recommendation System.

Responsibilities:
    - Configure the Streamlit page (must happen first, and only once).
    - Initialize session state used for login/authentication.
    - Render sidebar branding, logged-in status, and logout control.
    - Build an auth-gated navigation: logged-out users only ever see
      Login/Register; logged-in users only ever see the app pages.

Run with:
    streamlit run app.py
"""

import streamlit as st

from pages import Login, Register, Home, Recommendation, Search, Dashboard


def init_session_state() -> None:
    """
    Initialize all session_state keys used across the app, if they
    don't already exist. Runs on every script rerun but only sets
    defaults the first time.
    """
    defaults = {
        "logged_in": False,
        "user": None,  # Will hold {id, full_name, email, created_at} once logged in.
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def render_sidebar_branding() -> None:
    """Render the sidebar header, login status, and logout button."""
    with st.sidebar:
        st.markdown("## ✈️ Wherever Next")
        st.caption("AI-Powered Travel Recommendation System")
        st.divider()

        if st.session_state.logged_in and st.session_state.user:
            st.success(f"Logged in as **{st.session_state.user['full_name']}**")
            if st.button("🚪 Logout", use_container_width=True):
                logout()
            st.divider()


def logout() -> None:
    """Clear the session and return the user to the Login page."""
    st.session_state.logged_in = False
    st.session_state.user = None
    st.rerun()


def build_navigation() -> list:
    """
    Build the list of st.Page objects available to the user, based on
    whether they are currently logged in.

    Returns:
        A list of st.Page objects to pass to st.navigation().
    """
    if not st.session_state.logged_in:
        return [
            st.Page(Login.render, title="Login", icon="🔑", default=True),
            st.Page(Register.render, title="Register", icon="📝"),
        ]

    return [
        st.Page(Home.render, title="Home", icon="🏠", default=True),
        st.Page(Recommendation.render, title="Get Recommendations", icon="🧭"),
        st.Page(Search.render, title="Search Destinations", icon="🔍"),
        st.Page(Dashboard.render, title="Dashboard", icon="📊"),
    ]


def main() -> None:
    """Configure the page, initialize state, and run the router."""
    st.set_page_config(
        page_title="Wherever Next | Travel Recommender",
        page_icon="✈️",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    init_session_state()
    render_sidebar_branding()

    pages = build_navigation()
    router = st.navigation(pages, position="sidebar")
    router.run()


if __name__ == "__main__":
    main()
