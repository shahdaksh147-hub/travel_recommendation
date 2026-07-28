import streamlit as st

import pages.login as login
import pages.register as register
import pages.home as home
import pages.recommendation as recommendation
import pages.search as search
import pages.dashboard as dashboard

# ---------------------------------------------------
# Page Config
# ---------------------------------------------------
st.set_page_config(
    page_title="Wherever Next",
    page_icon="✈️",
    layout="wide",
)

# ---------------------------------------------------
# Session State
# ---------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None


# ---------------------------------------------------
# Logout
# ---------------------------------------------------
def logout():
    st.session_state.logged_in = False
    st.session_state.user = None
    st.rerun()


# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------
with st.sidebar:

    st.title("✈️ Wherever Next")
    st.caption("AI Travel Recommendation System")

    st.divider()

    if st.session_state.logged_in:

        st.success(
            f"Welcome\n\n{st.session_state.user['full_name']}"
        )

        page = st.radio(
            "Navigation",
            [
                "🏠 Home",
                "🧭 Recommendations",
                "🔍 Search",
                "📊 Dashboard",
            ],
        )

        st.divider()

        if st.button("🚪 Logout", use_container_width=True):
            logout()

    else:

        page = st.radio(
            "Account",
            [
                "Login",
                "Register",
            ],
        )


# ---------------------------------------------------
# Routing
# ---------------------------------------------------
if not st.session_state.logged_in:

    if page == "Login":
        login.render()

    else:
        register.render()

else:

    if page == "🏠 Home":
        home.render()

    elif page == "🧭 Recommendations":
        recommendation.render()

    elif page == "🔍 Search":
        search.render()

    elif page == "📊 Dashboard":
        dashboard.render()
