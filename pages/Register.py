"""
pages/Register.py
==================
Renders the Register page and handles creating a new user account.

All actual validation (email format, password strength, duplicate
email, matching confirmation) lives in auth.register_user() — this
module is purely responsible for collecting input and displaying
the result.
"""

import streamlit as st
from auth import register_user, MIN_PASSWORD_LENGTH


def render() -> None:
    """Render the Register page UI and handle form submission."""
    left, center, right = st.columns([1, 2, 1])

    with center:
        st.title("📝 Create Your Account")
        st.caption("Sign up to start getting AI-powered travel recommendations.")
        st.write("")

        with st.form("register_form"):
            full_name = st.text_input("Full Name", placeholder="Jane Doe")
            email = st.text_input("Email", placeholder="you@example.com")
            password = st.text_input("Password", type="password", placeholder="Choose a password")
            confirm_password = st.text_input(
                "Confirm Password", type="password", placeholder="Re-enter your password"
            )

            st.caption(
                f"Password must be at least {MIN_PASSWORD_LENGTH} characters long, "
                "and include at least one uppercase letter and one digit."
            )

            submitted = st.form_submit_button("Create Account", use_container_width=True, type="primary")

        if submitted:
            _handle_registration(full_name, email, password, confirm_password)

        st.divider()
        st.caption("Already have an account? Select **Login** from the sidebar.")


def _handle_registration(full_name: str, email: str, password: str, confirm_password: str) -> None:
    """
    Submit the registration form data to auth.register_user and
    display the outcome.

    Args:
        full_name: The user's full name.
        email: The user's email address.
        password: The chosen password.
        confirm_password: The re-entered password for confirmation.
    """
    success, message = register_user(full_name, email, password, confirm_password)

    if success:
        st.success(message)
        st.info("You can now switch to the **Login** page in the sidebar to sign in.")
    else:
        st.error(message)
