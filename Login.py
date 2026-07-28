"""
pages/Login.py
===============
Renders the Login page and handles authenticating an existing user.

On successful login, this module sets:
    st.session_state.logged_in = True
    st.session_state.user = {id, full_name, email, created_at}
which app.py's navigation uses to unlock the rest of the app.
"""

import streamlit as st
from auth import login_user


def render() -> None:
    """Render the Login page UI and handle form submission."""
    left, center, right = st.columns([1, 2, 1])

    with center:
        st.title("🔑 Welcome Back")
        st.caption("Log in to get personalized travel recommendations.")
        st.write("")

        with st.form("login_form"):
            email = st.text_input("Email", placeholder="you@example.com")
            password = st.text_input("Password", type="password", placeholder="Your password")
            submitted = st.form_submit_button("Login", use_container_width=True, type="primary")

        if submitted:
            _handle_login(email, password)

        st.divider()
        st.caption("Don't have an account? Select **Register** from the sidebar to create one.")


def _handle_login(email: str, password: str) -> None:
    """
    Validate the submitted credentials and update session state.

    Args:
        email: Email entered in the form.
        password: Password entered in the form.
    """
    if not email or not password:
        st.error("Please enter both your email and password.")
        return

    success, message, user_data = login_user(email, password)

    if success:
        st.session_state.logged_in = True
        st.session_state.user = user_data
        st.success(message)
        st.rerun()
    else:
        st.error(message)
