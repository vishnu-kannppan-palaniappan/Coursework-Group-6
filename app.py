import streamlit as st

if "users" not in st.session_state:
    st.session_state.users = {}

if "page" not in st.session_state:
    st.session_state.page = "auth"

if "user" not in st.session_state:
    st.session_state.user = None


def auth_page():
    st.title("Sign In / Sign Up")

    mode = st.radio("Mode", ["Sign In", "Sign Up"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button(mode):
        users = st.session_state.users

        if mode == "Sign In":
            if username in users and users[username] == password:
                st.session_state.user = username
                st.session_state.page = "home"
                st.rerun()
            else:
                st.error("Invalid login")

        else:  # Sign Up
            if username in users:
                st.error("User already exists")
            else:
                users[username] = password
                st.success("Account created. Now sign in.")


def home_page():
    st.title("Home Page")
    st.write(f"Welcome, {st.session_state.user}")

    if st.button("Log out"):
        st.session_state.user = None
        st.session_state.page = "auth"
        st.rerun()


if st.session_state.page == "auth":
    auth_page()
else:
    home_page()
