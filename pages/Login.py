import streamlit as st

from auth import login_user


def render():

    st.title("🔐 Login")

    st.write("Welcome back! Login to continue.")

    st.write("")

    with st.form("login_form"):

        email = st.text_input(
            "Email",
            placeholder="you@example.com"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        submitted = st.form_submit_button(
            "Login",
            use_container_width=True,
            type="primary"
        )

    if submitted:

        success, message, user = login_user(
            email,
            password
        )

        if success:

            st.session_state.logged_in = True

            st.session_state.user = user

            st.success(message)

            st.rerun()

        else:

            st.error(message)

    st.info(
        "Don't have an account? Select **Register** from the sidebar."
    )
