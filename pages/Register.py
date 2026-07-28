import streamlit as st

from auth import register_user


def render():

    st.title("📝 Create Account")

    st.write("Create your free account.")

    st.write("")

    with st.form("register_form"):

        full_name = st.text_input(
            "Full Name"
        )

        email = st.text_input(
            "Email"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        confirm = st.text_input(
            "Confirm Password",
            type="password"
        )

        submitted = st.form_submit_button(
            "Register",
            type="primary",
            use_container_width=True
        )

    if submitted:

        success, message = register_user(
            full_name,
            email,
            password,
            confirm
        )

        if success:

            st.success(message)

            st.balloons()

        else:

            st.error(message)

    st.info(
        "Already registered? Login from the sidebar."
    )
